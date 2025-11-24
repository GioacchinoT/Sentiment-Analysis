import pandas as pd  

def analisi_tematiche_transnazionali(df_tematico, temi_multilingua):
    
    print("\n")
    print("="*50, "> ANALISI TEMATICHE TRANSNAZONALI... (modulo 3_2)")
    
        
    # 1. DISTRIBUZIONE TEMI GLOBALE   
    distribuzione_temi_globale = {}
    for tema in temi_multilingua.keys():
        colonna_tema = f'tema_{tema}'
        conteggio = df_tematico[colonna_tema].sum()
        percentuale = (conteggio / len(df_tematico)) * 100
        distribuzione_temi_globale[tema] = {
            'conteggio': conteggio,
            'percentuale': percentuale,
            'descrizione': temi_multilingua[tema]['description']
        }
    
    # Ordina per frequenza
    temi_ordinati = sorted(distribuzione_temi_globale.items(), 
                          key=lambda x: x[1]['conteggio'], 
                          reverse=True)
    print("-" * 40)
    print("1. DISTRIBUZIONE TEMI:")
    print("-" * 40)
    for tema, stats in temi_ordinati:
        print(f"   > {tema}: {stats['conteggio']} commenti ({stats['percentuale']:.1f}%)")
        print(f"     {stats['descrizione']}")
    
    # 2. PROFILO TEMATICO PER NAZIONE
    print("\n 2. PROFILO TEMATICO PER NAZIONE")
    print("-" * 40)
    
    profilo_tematico_nazioni = {}
    
    for nazione in df_tematico['subreddit'].unique():
        df_nazione = df_tematico[df_tematico['subreddit'] == nazione]
        profilo = {}
        
        for tema in temi_multilingua.keys():
            colonna_tema = f'tema_{tema}'
            percentuale_nazione = (df_nazione[colonna_tema].sum() / len(df_nazione)) * 100
            profilo[tema] = percentuale_nazione
        
        profilo_tematico_nazioni[nazione] = profilo
    
    # Converti in DataFrame per analisi
    df_profilo_tematico = pd.DataFrame(profilo_tematico_nazioni).T
    
    print("Temi dominanti per nazione (top 3):")
    print("-" * 40)
    for nazione in df_profilo_tematico.index:
        temi_dominanti = df_profilo_tematico.loc[nazione].nlargest(3)
        print(f"\n   r/{nazione}:")
        for tema, percentuale in temi_dominanti.items():
            print(f"      > {tema}: {percentuale:.1f}%")
    
    return df_profilo_tematico, distribuzione_temi_globale
