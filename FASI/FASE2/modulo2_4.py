

def genera_report_fase2(metriche_nazioni, df):
    
    #Genera report riassuntivo della Fase 2
    
    print("\n")
    print("="*50, "> REPORT RIASSUNTIVO - FASE 2: ANALISI COMPARATIVA NAZIONI (modulo 2_4)")
    
    # Statistiche globali
    totale_commenti = len(df)
    nazioni_analizzate = len(metriche_nazioni)
    upvotes_totali = metriche_nazioni['upvotes_totali'].sum()
    
    print(f"-->>STATISTICHE GLOBALI:")
    print(f"   > Nazioni analizzate: {nazioni_analizzate}")
    print(f"   > Commenti totali: {totale_commenti:,}")
    print(f"   > Upvotes totali: {upvotes_totali:,}")
    print(f"   > Engagement ratio medio: {metriche_nazioni['engagement_ratio'].mean():.2f}")
    
    
    # Nazione più attiva
    nazione_attiva = metriche_nazioni.nlargest(1, 'commenti_totali').index[0]
    commenti_attiva = metriche_nazioni.loc[nazione_attiva, 'commenti_totali']
    print(f"   > Nazione più attiva: r/{nazione_attiva} ({commenti_attiva} commenti)")
    
    # Nazione con miglior engagement
    nazione_engagement = metriche_nazioni.nlargest(1, 'engagement_ratio').index[0]
    engagement_val = metriche_nazioni.loc[nazione_engagement, 'engagement_ratio']
    print(f"   > Miglior engagement: r/{nazione_engagement} ({engagement_val:.2f} upvotes/commento)")
    
    # Nazione più virale
    nazione_virale = metriche_nazioni.nlargest(1, 'upvote_max').index[0]
    upvote_max = metriche_nazioni.loc[nazione_virale, 'upvote_max']
    print(f"   > Commento più virale: r/{nazione_virale} ({upvote_max} upvotes)")
    
    # Variabilità tra nazioni
    cv_engagement = (metriche_nazioni['engagement_ratio'].std() / metriche_nazioni['engagement_ratio'].mean()) * 100
    print(f"   > Variabilità engagement: {cv_engagement:.1f}% (alta variabilità tra nazioni)")
    
    # Correlazioni 
    correlazione_volume_engagement = metriche_nazioni['commenti_totali'].corr(metriche_nazioni['engagement_ratio'])
    print(f"   > Correlazione volume-engagement: {correlazione_volume_engagement:.3f}")
    
    metriche_nazioni.to_csv(f"report e grafici generati/metriche_nazioni.csv")
    print(f"\n ---->      Metriche salvate: report e grafici generati/metriche_nazioni.csv")
