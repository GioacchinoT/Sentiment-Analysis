from datetime import datetime

def analisi_sentiment_per_post(df_sentiment):

    print("\n" + "="*60)
    print("ANALISI SENTIMENT PER POST - NAZIONALMENTE")
    print("="*60)
    
    risultati_per_nazione = {}
    
    for nazione in df_sentiment['subreddit'].unique():
        df_nazione = df_sentiment[df_sentiment['subreddit'] == nazione]
        
        # Raggruppa per post
        sentiment_per_post = df_nazione.groupby(['post_id', 'post_title']).agg({
            'polarita': ['mean', 'std', 'count'],
            'soggettivita': 'mean',
            'comment_score': 'sum',
            'comment_id': 'count'
        }).round(3)
        
        # Appiattisci colonne
        sentiment_per_post.columns = [
            'sentiment_medio', 'sentiment_std', 'commenti_analizzati_sentiment',
            'soggettivita_media', 'engagement_totale', 'totale_commenti'
        ]
        
        # Calcola polarizzazione (alta std = alta polarizzazione)
        sentiment_per_post['indice_polarizzazione'] = (
            sentiment_per_post['sentiment_std'] * 
            (sentiment_per_post['commenti_analizzati_sentiment'] / sentiment_per_post['commenti_analizzati_sentiment'].max())
        ).round(3)
        
        # Classifiche
        post_piu_positivi = sentiment_per_post.nlargest(5, 'sentiment_medio')
        post_piu_negativi = sentiment_per_post.nsmallest(5, 'sentiment_medio')
        post_piu_polarizzati = sentiment_per_post.nlargest(5, 'indice_polarizzazione')
        
        risultati_per_nazione[nazione] = {
            'tutti_i_post': sentiment_per_post,
            'piu_positivi': post_piu_positivi,
            'piu_negativi': post_piu_negativi, 
            'piu_polarizzati': post_piu_polarizzati
        }
        
        # Stampa risultati per nazione
        print(f"\n r/{nazione.upper()}:")
        print(f"   Post totali analizzati: {len(sentiment_per_post)}")
        
        if not post_piu_positivi.empty:
            print(f"   > Post più POSITIVO: {post_piu_positivi.iloc[0]['sentiment_medio']:.3f}")
            print(f"   > Post più NEGATIVO: {post_piu_negativi.iloc[0]['sentiment_medio']:.3f}")
            print(f"   > Post più POLARIZZATO: {post_piu_polarizzati.iloc[0]['indice_polarizzazione']:.3f}")

            if nazione.lower() == 'italy' or nazione.lower() == 'de' or nazione.lower() == 'denmark':
                print(f"\n{'='*80}")
                print(f"🇮🇹 ANALISI DETTAGLIATA - r/{nazione.lower()}")
                print(f"{'='*80}")
                
                print(f"\n-------------- I 5 POST PIÙ NEGATIVI:")
                print("-" * 80)
                
                if not post_piu_negativi.empty:
                    for i, (post_id, stats) in enumerate(post_piu_negativi.iterrows(), 1):
                        titolo = post_id[1]
                        sentiment = stats['sentiment_medio']
                        polarizzazione = stats['sentiment_std']
                        commenti = stats['totale_commenti']
                        engagement = stats['engagement_totale']
                        
                        print(f"\n{i} [NEGATIVITÀ: {sentiment:.3f}] - Polarizzazione: {polarizzazione:.3f}")
                        print(f"   - {titolo}")
                        print(f"   - {commenti} commenti | {engagement} upvotes totali")
                        print(f"   - Post ID: {post_id[0]}")
                        print("-" * 60)
                else:
                    print("   Nessun post negativo identificato")
                
                print(f"\n--------- I 5 POST PIÙ POLARIZZATI:")
                print("-" * 80)
                
                if not post_piu_polarizzati.empty:
                    for i, (post_id, stats) in enumerate(post_piu_polarizzati.iterrows(), 1):
                        titolo = post_id[1]
                        polarizzazione_indice = stats['indice_polarizzazione']
                        polarizzazione_std = stats['sentiment_std']
                        sentiment = stats['sentiment_medio']
                        commenti = stats['totale_commenti']
                        engagement = stats['engagement_totale']
                        
                        # Determina se prevalentemente positivo/negativo/neutro
                        if sentiment > 0.1:
                            tendenza = "POSITIVA"
                        elif sentiment < -0.1:
                            tendenza = "NEGATIVA"
                        else:
                            tendenza = "NEUTRA"
                        
                        print(f"\n{i} [POLARIZZAZIONE: {polarizzazione_indice:.3f}] - Tendenza: {tendenza}")
                        print(f"   - {titolo}")
                        print(f"   - Deviazione: {polarizzazione_std:.3f} | Sentiment: {sentiment:.3f}")
                        print(f"   - {commenti} commenti | {engagement} upvotes totali")
                        print(f"   - Post ID: {post_id[0]}")
                        print("-" * 60)
                else:
                    print("   Nessun post polarizzato identificato")
                

    
    return risultati_per_nazione

def genera_report_fase4(df_sentiment, sentiment_per_nazione, df_sentiment_temi, polarizzazione_per_nazione):
    """
    Genera report completo della Fase 4
    """
    
    print("\n")
    print("="*50, "> REPORT RIASSUNTIVO - FASE 4: ANALISI DI SENTIMENT COMPARATA(modulo 4_6)")
    
    # Statistiche globali
    totale_commenti = len(df_sentiment)
    polarita_media_globale = df_sentiment['polarita'].mean()
    soggettivita_media_globale = df_sentiment['soggettivita'].mean()
    
    print(f"STATISTICHE GLOBALI:")
    print("-" *40)
    print(f"   > Commenti analizzati: {totale_commenti:,}")
    print(f"   > Polarità media globale: {polarita_media_globale:.3f}")
    print(f"   > Soggettività media globale: {soggettivita_media_globale:.3f}")
    print(f"   > Nazioni con sentiment positivo: {(sentiment_per_nazione['polarita_media'] > 0).sum()}")
    print(f"   > Nazioni con sentiment negativo: {(sentiment_per_nazione['polarita_media'] < 0).sum()}")
    
    # Insights principali
    print(f"\nINSIGHTS PRINCIPALI:")
    print("-" *40)
    
    
    # Nazione più positiva/negativa
    nazione_piu_positiva = sentiment_per_nazione.nlargest(1, 'polarita_media').index[0]
    nazione_piu_negativa = sentiment_per_nazione.nsmallest(1, 'polarita_media').index[0]
    print(f"   > Nazione più positiva: r/{nazione_piu_positiva} "
          f"({sentiment_per_nazione.loc[nazione_piu_positiva, 'polarita_media']:.3f})")
    print(f"   > Nazione più negativa: r/{nazione_piu_negativa} "
          f"({sentiment_per_nazione.loc[nazione_piu_negativa, 'polarita_media']:.3f})")
    
    # Tema più positivo/negativo
    if not df_sentiment_temi.empty:
        tema_piu_positivo = df_sentiment_temi.nlargest(1, 'polarita_media')['tema'].iloc[0]
        tema_piu_negativo = df_sentiment_temi.nsmallest(1, 'polarita_media')['tema'].iloc[0]
        print(f"   > Tema più positivo: {tema_piu_positivo}")
        print(f"   > Tema più negativo: {tema_piu_negativo}")
    
    # Polarizzazione
    nazione_piu_polarizzata = max(polarizzazione_per_nazione.items(), 
                                 key=lambda x: x[1]['indice_polarizzazione'])[0]
    print(f"   > Nazione più polarizzata: r/{nazione_piu_polarizzata}")
    
    
    # Pattern regionali
    print(f"\n PATTERN REGIONALI:")
    print("-" *40)
    
    # Raggruppa per area geografica
    aree_geografiche = {
        'Europa Occidentale': ['france', 'unitedkingdom', 'ireland', 'belgium', 'netherlands'],
        'Europa Centrale': ['de', 'austria', 'switzerland', 'czech'], 
        'Europa Meridionale': ['italy', 'spain', 'portugal', 'greece'],
        'Europa Settentrionale': ['sweden', 'norway', 'denmark', 'finland'],
        'Europa Orientale': ['poland', 'hungary', 'romania']
    }
    
    sentiment_per_area = {}
    for area, nazioni in aree_geografiche.items():
        nazioni_presenti = [n for n in nazioni if n in sentiment_per_nazione.index]
        if nazioni_presenti:
            polarita_media = sentiment_per_nazione.loc[nazioni_presenti, 'polarita_media'].mean()
            sentiment_per_area[area] = polarita_media
            print(f"   > {area}: {polarita_media:.3f} ({len(nazioni_presenti)} nazioni)")
    
    # Area più positiva/negativa
    if sentiment_per_area:
        area_piu_positiva = max(sentiment_per_area.items(), key=lambda x: x[1])[0]
        area_piu_negativa = min(sentiment_per_area.items(), key=lambda x: x[1])[0]
        print(f"   > Area più positiva: {area_piu_positiva}")
        print(f"   > Area più negativa: {area_piu_negativa}")
    
    # Correlazioni significative
    print(f"\n CORRELAZIONI SIGNIFICATIVE:")
    print("-" *40)
    
    # Correlazione polarità-engagement
    correlazione_globale = df_sentiment['polarita'].corr(df_sentiment['comment_score'])
    print(f"   > Correlazione polarità-engagement globale: {correlazione_globale:.3f}")
    
    # Correlazione per nazioni significative
    correlazioni_nazionali = []
    for nazione in df_sentiment['subreddit'].unique():
        df_nazione = df_sentiment[df_sentiment['subreddit'] == nazione]
        if len(df_nazione) > 20:
            correlazione = df_nazione['polarita'].corr(df_nazione['comment_score'])
            correlazioni_nazionali.append((nazione, correlazione))
    
    correlazioni_nazionali.sort(key=lambda x: abs(x[1]), reverse=True)
    
    print(f"   > Correlazioni più forti per nazione:")
    for nazione, corr in correlazioni_nazionali[:3]:
        print(f"      r/{nazione}: {corr:.3f}")
    
    # Salva dataset con sentiment
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    df_sentiment.to_csv(f"report e grafici generati/dataset_sentiment_completo.csv", index=False, encoding='utf-8')
    print(f"\n-----> Dataset con sentiment salvato: report e grafici generati/dataset_sentiment_completo.csv")
    
    # Salva metriche sentiment per nazione
    sentiment_per_nazione.to_csv(f"report e grafici generati/metriche_sentiment_nazioni.csv")
    print(f"-----> Metriche sentiment per nazione salvate: report e grafici generati/metriche_sentiment_nazioni.csv")
    
    # Salva analisi temi-sentiment
    if not df_sentiment_temi.empty:
        df_sentiment_temi.to_csv(f"report e grafici generati/analisi_temi_sentiment.csv", index=False)
        print(f"----> Analisi temi-sentiment salvata: report e grafici generati/analisi_temi_sentiment.csv")
    

    return sentiment_per_area