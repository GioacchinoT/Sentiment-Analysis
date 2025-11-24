
def genera_report_fase5_e_conclusione(df_temporale, andamento_giornaliero, evoluzione_nazionale, eventi_significativi, risultati_predittivi):
    """
    Genera report finale della Fase 5 e conclusione generale dell'analisi
    """
    print("\n")
    print("="*50, "> REPORTO FINALE - FASE 5: ANALISI TEMPORALE E EVOLUZIONE (modulo 5_5)")
    
    # Statistiche temporali
    giorni_analizzati = len(andamento_giornaliero)
    commenti_totali = len(df_temporale)
    volume_medio_giornaliero = commenti_totali / giorni_analizzati
    
    print(f"--> STATISTICHE TEMPORALI:")
    print("-" *40)
    print(f"   > Periodo analizzato: {giorni_analizzati} giorni")
    print(f"   > Commenti totali: {commenti_totali:,}")
    print(f"   > Volume medio giornaliero: {volume_medio_giornaliero:.1f} commenti")
    print(f"   > Eventi significativi identificati: {len(eventi_significativi)}")
    
    # Insights temporali principali
    print("-" *40)
    print(f" INSIGHTS TEMPORALI PRINCIPALI:")
    print("-" *40)
    
    # Trend globale
    trend_volume = risultati_predittivi['trend_volume_globale']
    trend_sentiment = risultati_predittivi['trend_sentiment_globale']
    
    direzione_volume = "CRESCITA" if trend_volume > 0 else "DECRESCITA"
    direzione_sentiment = "MIGLIORAMENTO" if trend_sentiment > 0 else "PEGGIORAMENTO"
    
    print(f"   > Trend volume: {direzione_volume} ({trend_volume:+.2f} commenti/giorno)")
    print(f"   > Trend sentiment: {direzione_sentiment} ({trend_sentiment:+.4f}/giorno)")
    
    # Pattern identificati
    ora_piu_attiva = df_temporale.groupby('ora_giorno')['comment_id'].count().idxmax()
    giorno_piu_attivo = df_temporale.groupby('giorno_settimana')['comment_id'].count().idxmax()
    
    print(f"   > Ora più attiva: {ora_piu_attiva}:00")
    print(f"   > Giorno più attivo: {giorno_piu_attivo}")
    
    # Nazioni con evoluzione più interessante
    if evoluzione_nazionale:
        nazione_crescita_massima = max(evoluzione_nazionale.items(), key=lambda x: x[1]['trend_volume'])
        nazione_miglior_sentiment = max(evoluzione_nazionale.items(), key=lambda x: x[1]['trend_sentiment'])
        
        print(f"   > Nazione con crescita più rapida: r/{nazione_crescita_massima[0]}")
        print(f"   > Nazione con miglioramento sentiment: r/{nazione_miglior_sentiment[0]}")
    
    # CONCLUSIONE GENERALE DELL'INTERA ANALISI
    print("\n" + "="*80)
    print(" CONCLUSIONE GENERALE - ANALISI COMPLETA 5 FASI")
    print("="*80)
    
    print(f"\n -----> SYNTHESIS DEI RISULTATI OTTENUTI:")
    
    # Fase 1 - Raccolta Dati
    nazioni_analizzate = df_temporale['subreddit'].nunique()
    commenti_totali = len(df_temporale)
    print(f"--> FASE 1 - RACCOLTA DATI:")
    print("-" *40)
    print(f"   > {nazioni_analizzate} nazioni europee analizzate")
    print(f"   > {commenti_totali:,} commenti raccolti")
    print(f"   > Periodo: {df_temporale['data_datetime'].min().strftime('%d/%m/%Y')} - {df_temporale['data_datetime'].max().strftime('%d/%m/%Y')}")
    
    # Fase 2 - Analisi Comparativa
    engagement_medio = df_temporale['comment_score'].mean()
    nazione_top_engagement = df_temporale.groupby('subreddit')['comment_score'].mean().idxmax()
    print(f"\n--> FASE 2 - ANALISI COMPARATIVA:")
    print("-" *40)
    print(f"   > Engagement medio: {engagement_medio:.1f} upvotes/commento")
    print(f"   > Nazione con miglior engagement: r/{nazione_top_engagement}")
    print(f"   > Cluster identificati: 4 tipologie di comunità")
    
    # Fase 3 - Analisi Tematica
    temi_identificati = len([col for col in df_temporale.columns if col.startswith('tema_')])
    tema_piu_discusso = max([col for col in df_temporale.columns if col.startswith('tema_')], 
                           key=lambda x: df_temporale[x].sum())
    print(f"\n --> FASE 3 - ANALISI TEMATICA:")
    print("-" *40)
    print(f"   > {temi_identificati} temi monitorati")
    print(f"   > Tema più discusso: {tema_piu_discusso.replace('tema_', '')}")
    
    # Fase 4 - Analisi Sentiment
    sentiment_medio_globale = df_temporale['polarita'].mean()
    nazione_piu_positiva = df_temporale.groupby('subreddit')['polarita'].mean().idxmax()
    nazione_piu_negativa = df_temporale.groupby('subreddit')['polarita'].mean().idxmin()
    print(f"\n --> FASE 4 - ANALISI SENTIMENT:")
    print("-" *40)
    print(f"   > Sentiment medio globale: {sentiment_medio_globale:.3f}")
    print(f"   > Nazione più positiva: r/{nazione_piu_positiva}")
    print(f"   > Nazione più negativa: r/{nazione_piu_negativa}")
    
    # Fase 5 - Analisi Temporale
    giorni_analizzati_fase5 = len(andamento_giornaliero)
    numero_eventi_significativi = len(eventi_significativi)  # ⚠️ CAMBIA NOME VARIABILE
    print(f"\n--> FASE 5 - ANALISI TEMPORALE:")
    print("-" *40)
    print(f"   > {giorni_analizzati_fase5} giorni analizzati")
    print(f"   > {numero_eventi_significativi} eventi significativi identificati")
    print(f"   > Trend volume: {risultati_predittivi['trend_volume_globale']:+.2f} commenti/giorno")
    print(f"   > Proiezioni per i prossimi 7 giorni generate")
    
    print(f"\n ==================================== INSIGHTS TRANSVERSALI PRINCIPALI:")
    
    # 1. Pattern Geografico-Culturali
    print("-" *40)
    print(f"1. --> PATTERN GEOGRAFICO-CULTURALI:")
    print("-" *40)
    # Raggruppa per macro-aree
    aree_europee = {
        'Nordica': ['sweden', 'norway', 'denmark', 'finland'],
        'Occidentale': ['france', 'unitedkingdom', 'ireland', 'netherlands', 'belgium'],
        'Centrale': ['de', 'austria', 'switzerland', 'czech'],
        'Meridionale': ['italy', 'spain', 'portugal', 'greece'],
        'Orientale': ['poland', 'hungary', 'romania']
    }
    
    for area, nazioni in aree_europee.items():
        nazioni_presenti = [n for n in nazioni if n in df_temporale['subreddit'].unique()]
        if nazioni_presenti:
            df_area = df_temporale[df_temporale['subreddit'].isin(nazioni_presenti)]
            sentiment_area = df_area['polarita'].mean()
            engagement_area = df_area['comment_score'].mean()
            print(f"   > {area}: sentiment {sentiment_area:.3f}, engagement {engagement_area:.1f}")
    
    # 2. Relazione tra Metriche
    print("-" *40)
    print(f"\n --> 2. RELAZIONI TRA METRICHE CHIAVE:")
    print("-" *40)
    
    correlazione_sentiment_engagement = df_temporale['polarita'].corr(df_temporale['comment_score'])
    correlazione_volume_sentiment = andamento_giornaliero['volume_commenti'].corr(andamento_giornaliero['sentiment_medio'])
    
    print(f"   > Correlazione sentiment-engagement: {correlazione_sentiment_engagement:.3f}")
    print(f"   > Correlazione volume-sentiment: {correlazione_volume_sentiment:.3f}")
    
    if correlazione_sentiment_engagement > 0.1:
        print(f"     > I commenti positivi tendono a ricevere più engagement")
    elif correlazione_sentiment_engagement < -0.1:
        print(f"     > I commenti negativi tendono a ricevere più engagement")
    else:
        print(f"     > Nessuna correlazione forte tra sentiment e engagement")
    
    # 3. Dinamiche Temporali Critiche
    print("-" *40)
    print(f"\n --> 3. DINAMICHE TEMPORALI CRITICHE:")
    print("-" *40)
    
    if eventi_significativi and len(eventi_significativi) > 0:  
        evento_piu_importante = max(eventi_significativi, key=lambda x: x['volume'])
        print(f"    > Evento più significativo: {evento_piu_importante['data']}")
        print(f"    > Volume: {evento_piu_importante['volume']} commenti")
        print(f"    > Sentiment: {evento_piu_importante['sentiment']:.3f}")
        if evento_piu_importante['temi_dominanti']:
            tema_principale = max(evento_piu_importante['temi_dominanti'].items(), key=lambda x: x[1])
            print(f"     Tema dominante: {tema_principale[0]} ({tema_principale[1]:.1f}%)")
    else:
        print(f"   > Nessun evento significativo identificato")
    


    print(f"\n --> SALVATAGGIO DATASET FINALE...")
    
    
    # Dataset completo
    df_temporale.to_csv(f"report e grafici generati/dataset_analisi_completa.csv", index=False, encoding='utf-8')
    print(f"   - Dataset completo: report e grafici generati/dataset_analisi_completa.csv")
    
    # Report riassuntivo
    with open(f"report e grafici generati/report_finale_analisi.txt", 'w', encoding='utf-8') as f:
        f.write("REPORT FINALE - ANALISI DISCUSSIONI GAZA IN 20 NAZIONI EUROPEE\n")
        f.write("="*60 + "\n\n")
        f.write(f"Periodo analisi: {df_temporale['data_datetime'].min()} - {df_temporale['data_datetime'].max()}\n")
        f.write(f"Nazioni analizzate: {nazioni_analizzate}\n")
        f.write(f"Commenti totali: {commenti_totali:,}\n")
        f.write(f"Sentiment medio globale: {sentiment_medio_globale:.3f}\n")
        f.write(f"Engagement medio: {engagement_medio:.1f}\n\n")

    
    print(f"   > Reprt finale: report e grafici generati/report_finale_analisi.txt")
    print(f"\n" + "="*80)
    print(" ANALISI COMPLETATA ")
    print("="*80)
