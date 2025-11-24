import numpy as np
import warnings
warnings.filterwarnings('ignore')

def analisi_evoluzione_temporale(df_temporale):
    """
    Analisi evoluzione temporale 
    """
    print("\n")
    print("="*50, "> ANALISI EVOLUZIONE TEMPORALE (modulo 5_2)")
    
    
    # 1. ANDAMENTO GIORNALIERO GLOBALE
    print("-" *40)
    print("1. ANDAMENTO GIORNALIERO GLOBALE ")
    print("-" *40)
    
    # Aggregazione giornaliera 
    andamento_giornaliero = df_temporale.groupby('data_giorno').agg({
        'comment_id': 'count',
        'polarita': 'mean',
        'soggettivita': 'mean',
        'comment_score': 'mean'
    }).rename(columns={
        'comment_id': 'volume_commenti',
        'polarita': 'sentiment_medio',
        'soggettivita': 'soggettivita_media',
        'comment_score': 'engagement_medio'
    })
    
    # Calcola metriche di tendenza SOLO se abbastanza giorni
    if len(andamento_giornaliero) > 7:
        andamento_giornaliero['volume_rolling_7d'] = andamento_giornaliero['volume_commenti'].rolling(window=7).mean()
        andamento_giornaliero['sentiment_rolling_7d'] = andamento_giornaliero['sentiment_medio'].rolling(window=7).mean()
    
    # Statistiche volume
    volume_mean = andamento_giornaliero['volume_commenti'].mean()
    volume_std = andamento_giornaliero['volume_commenti'].std()
    
    print("-" *40)
    print(f"--> Statistiche volume giornaliero :")
    print(f"   > Media: {volume_mean:.1f} commenti/giorno")
    print(f"   > Deviazione standard: {volume_std:.1f}")
    print(f"   > Giorni analizzati: {len(andamento_giornaliero)}")
    
    # Identifica picchi significativi
    if volume_std > 0:
        picchi_volume = andamento_giornaliero[andamento_giornaliero['volume_commenti'] > volume_mean + volume_std]
        print(f"   > Giorni con picco: {len(picchi_volume)}")
        
        if not picchi_volume.empty:
            print(f"      ---> Picchi di volume significativi:")
            for data, stats in picchi_volume.nlargest(5, 'volume_commenti').iterrows():
                print(f"          > {data}: {stats['volume_commenti']} commenti (sentiment: {stats['sentiment_medio']:.3f})")
    
    # 2. ANALISI PER NAZIONE NEL TEMPO
    print("-" *40)
    print(" 2. EVOLUZIONE TEMPORALE PER NAZIONE ")
    print("-" * 40)
    
    evoluzione_nazionale = {}
    
    for nazione in df_temporale['subreddit'].unique():
        df_nazione = df_temporale[df_temporale['subreddit'] == nazione]
        
        andamento_nazione = df_nazione.groupby('data_giorno').agg({
            'comment_id': 'count',
            'polarita': 'mean',
            'comment_score': 'mean'
        }).rename(columns={
            'comment_id': 'volume',
            'polarita': 'sentiment',
            'comment_score': 'engagement'
        })
        
        # Calcola trend solo se ci sono abbastanza dati
        if len(andamento_nazione) > 5:
            x = np.arange(len(andamento_nazione))
            y_volume = andamento_nazione['volume'].values
            y_sentiment = andamento_nazione['sentiment'].values
            
            trend_volume = np.polyfit(x, y_volume, 1)[0] if len(y_volume) > 1 else 0
            trend_sentiment = np.polyfit(x, y_sentiment, 1)[0] if len(y_sentiment) > 1 else 0
            
            evoluzione_nazionale[nazione] = {
                'andamento': andamento_nazione,
                'trend_volume': trend_volume,
                'trend_sentiment': trend_sentiment,
                'volume_medio': andamento_nazione['volume'].mean(),
                'giorni_attivi': len(andamento_nazione)
            }
    
    # Classifica nazioni per trend
    if evoluzione_nazionale:
        nazioni_crescita_volume = sorted(evoluzione_nazionale.items(), 
                                        key=lambda x: x[1]['trend_volume'], reverse=True)
        nazioni_crescita_sentiment = sorted(evoluzione_nazionale.items(), 
                                           key=lambda x: x[1]['trend_sentiment'], reverse=True)
        
        print("Nazioni con MAGGIORE CRESCITA di volume:")
        print("-" *40)
        for nazione, stats in nazioni_crescita_volume[:5]:
            print(f"   > r/{nazione}: +{stats['trend_volume']:.2f} commenti/giorno")
        
        print("\nNazioni con MAGGIORE CRESCITA di sentiment:")
        print("-" *40)
        for nazione, stats in nazioni_crescita_sentiment[:5]:
            print(f"   < r/{nazione}: +{stats['trend_sentiment']:.3f} sentiment/giorno")
    
    # 3. IDENTIFICAZIONE EVENTI CHIAVE 
    print("-" *40)
    print("3. IDENTIFICAZIONE EVENTI CHIAVE ")
    print("-" * 40)
    
    eventi_significativi = []
    
    if len(andamento_giornaliero) > 1 and volume_std > 0:
        for data in andamento_giornaliero.index:
            stats_giorno = andamento_giornaliero.loc[data]
            
            # Definisci criteri per evento significativo
            volume_anomalo = stats_giorno['volume_commenti'] > volume_mean + volume_std
            sentiment_estremo = abs(stats_giorno['sentiment_medio']) > 0.2
            
            if volume_anomalo or sentiment_estremo:
                # Analizza composizione tematica del giorno
                df_giorno = df_temporale[df_temporale['data_giorno'] == data]
                temi_giorno = {}
                
                for colonna_tema in [col for col in df_temporale.columns if col.startswith('tema_')]:
                    tema = colonna_tema.replace('tema_', '')
                    percentuale_tema = (df_giorno[colonna_tema].sum() / len(df_giorno)) * 100
                    if percentuale_tema > 10:  # Soglia 10%
                        temi_giorno[tema] = percentuale_tema
                
                eventi_significativi.append({
                    'data': data,
                    'volume': stats_giorno['volume_commenti'],
                    'sentiment': stats_giorno['sentiment_medio'],
                    'temi_dominanti': temi_giorno,
                    'tipo_evento': 'volume_anomalo' if volume_anomalo else 'sentiment_estremo'
                })
        
        print("Eventi significativi identificati:")
        for evento in sorted(eventi_significativi, key=lambda x: x['volume'], reverse=True)[:5]:
            print(f"   • {evento['data']}: {evento['volume']} commenti, sentiment {evento['sentiment']:.3f}")
            if evento['temi_dominanti']:
                tema_principale = max(evento['temi_dominanti'].items(), key=lambda x: x[1])
                print(f"     Tema dominante: {tema_principale[0]} ({tema_principale[1]:.1f}%)")
    else:
        print("   Dati insufficienti per identificare eventi significativi")
    
    # 4. ANALISI PATTERN TEMPORALI 
    print("-" *40)
    print("4. ANALISI PATTERN TEMPORALI ")
    print("-" * 40)
    
    # Pattern giornaliero
    pattern_giornaliero = df_temporale.groupby('ora_giorno').agg({
        'comment_id': 'count',
        'polarita': 'mean',
        'comment_score': 'mean'
    })
    
    if not pattern_giornaliero.empty:
        pattern_giornaliero['percentuale_totale'] = (pattern_giornaliero['comment_id'] / len(df_temporale)) * 100
        
        ora_piu_attiva = pattern_giornaliero['comment_id'].idxmax()
        attivita_massima = pattern_giornaliero['comment_id'].max()
        
        print(f"Pattern di attività giornaliero:")
        print(f"   > Ora più attiva: {ora_piu_attiva}:00 ({attivita_massima} commenti)")
        print(f"   > Distribuzione per fasce orarie:")
        
        for periodo in ['Notte', 'Mattina', 'Pomeriggio', 'Sera']:
            df_periodo = df_temporale[df_temporale['periodo_giornaliero'] == periodo]
            if len(df_periodo) > 0:
                percentuale = (len(df_periodo) / len(df_temporale)) * 100
                sentiment_periodo = df_periodo['polarita'].mean()
                print(f"      {periodo}: {percentuale:.1f}% (sentiment: {sentiment_periodo:.3f})")
    
    # Pattern settimanale
    pattern_settimanale = df_temporale.groupby('giorno_settimana').agg({
        'comment_id': 'count',
        'polarita': 'mean'
    })
    
    if not pattern_settimanale.empty:
        # Riordina giorni della settimana
        ordine_giorni = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pattern_settimanale = pattern_settimanale.reindex(ordine_giorni)
        
        giorno_piu_attivo = pattern_settimanale['comment_id'].idxmax()
        
        print(f"\nPattern settimanale:")
        print("-" *40)
        print(f"   > Giorno più attivo: {giorno_piu_attivo}")
        for giorno in ordine_giorni:
            if giorno in pattern_settimanale.index:
                stats = pattern_settimanale.loc[giorno]
                print(f"      {giorno[:3]}: {stats['comment_id']} commenti (sentiment: {stats['polarita']:.3f})")
    
    return andamento_giornaliero, evoluzione_nazionale, eventi_significativi, pattern_giornaliero, pattern_settimanale

