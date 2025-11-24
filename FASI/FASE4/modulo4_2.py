import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def analisi_sentiment_comparata(df_sentiment):

    print("\n")
    print("="*50, ">  ANALISI SENTIMENT COMPARATA TRA NAZIONI... (modulo 4_2) ")
    
    # 1. STATISTICHE SENTIMENT GLOBALI
    print("-" * 40)
    print("1. STATISTICHE SENTIMENT GLOBALI")
    print("-" * 40)
    
    stats_globali = {
        'polarita_media': df_sentiment['polarita'].mean(),
        'polarita_mediana': df_sentiment['polarita'].median(),
        'polarita_std': df_sentiment['polarita'].std(),
        'soggettivita_media': df_sentiment['soggettivita'].mean(),
        'distribuzione_categorie': df_sentiment['categoria_sentiment'].value_counts(normalize=True) * 100 #Distribuzione categorie globale
    }
    
    print(f"Polarita globale: {stats_globali['polarita_media']:.3f} (dev_std={stats_globali['polarita_std']:.3f})")
    print(f"Soggettività globale: {stats_globali['soggettivita_media']:.3f}")
    print("\nDistribuzione categorie sentiment:")
    for categoria, percentuale in stats_globali['distribuzione_categorie'].items():
        print(f"   > {categoria}: {percentuale:.1f}%")
    
    # 2. SENTIMENT PER NAZIONE
    print("-" * 40)
    print("2. ANALISI PER NAZIONE --> SENTIMENT PER NAZIONE")
    print("-" * 40)
    
    sentiment_per_nazione = df_sentiment.groupby('subreddit').agg({
        'polarita': ['mean', 'std', 'count', lambda x: (x > 0.1).sum()/len(x)*100],
        'soggettivita': 'mean',
        'categoria_sentiment': lambda x: (x == 'positivo').sum()/len(x)*100 # ---->Percentuale commenti positivi per nazione 
    }).round(3)
    
    sentiment_per_nazione.columns = [
        'polarita_media', 'polarita_std', 'commenti_analizzati', 'percentuale_positivi',
        'soggettivita_media', 'percentuale_categoria_positiva'
    ]
    
    # Aggiungi ranking
    sentiment_per_nazione['ranking_polarita'] = sentiment_per_nazione['polarita_media'].rank(ascending=False)
    sentiment_per_nazione['ranking_soggettivita'] = sentiment_per_nazione['soggettivita_media'].rank(ascending=False)
    
    print("Nazioni ordinate per polarità media (dalla più positiva):")
    print("-" * 40)
    nazioni_ordinate = sentiment_per_nazione.sort_values('polarita_media', ascending=False)
    for nazione, stats in nazioni_ordinate.head(10).iterrows():
        print(f"   • r/{nazione}: {stats['polarita_media']:.3f} "
              f"(±{stats['polarita_std']:.3f}, "
              f"{stats['percentuale_positivi']:.1f}% positivi)")
    
    # 3. SENTIMENT PER TEMA E NAZIONE
    print("-" * 40)
    print("3. SENTIMENT PER COPPIA TEMA-NAZIONE")
    print("-" * 40)
    
    # Seleziona colonne tema
    colonne_temi = [col for col in df_sentiment.columns if col.startswith('tema_')]

    risultati_tema_nazione = []

    for colonna_tema in colonne_temi:
        tema = colonna_tema.replace('tema_', '')
        
        for nazione in df_sentiment['subreddit'].unique():
            df_filtro = df_sentiment[(df_sentiment[colonna_tema] == 1) & 
                                (df_sentiment['subreddit'] == nazione)]
            
            if len(df_filtro) >= 3:  # Almeno 3 commenti per statistica
                polarita_media = df_filtro['polarita'].mean()
                soggettivita_media = df_filtro['soggettivita'].mean()
                conteggio = len(df_filtro)
                
                risultati_tema_nazione.append({
                    'tema': tema,
                    'nazione': nazione,
                    'polarita_media': polarita_media,
                    'soggettivita_media': soggettivita_media,
                    'commenti': conteggio
                })

    # Converti in DataFrame
    df_sentiment_temi = pd.DataFrame(risultati_tema_nazione)

    # Trova combinazioni estreme - CORREZIONE APPLICATA
    combinazioni_piu_positive = df_sentiment_temi.nlargest(5, 'polarita_media')
    combinazioni_piu_negative = df_sentiment_temi.nsmallest(5, 'polarita_media')

    print("Combinazioni TEMA-NAZIONE più POSITIVE:")
    print("-" * 40)
    for _, combo in combinazioni_piu_positive.iterrows():
        print(f"   > r/{combo['nazione']} - {combo['tema']}: {combo['polarita_media']:.3f} ({combo['commenti']} commenti)")  # AGGIUNTO INFO

    print("\nCombinazioni TEMA-NAZIONE più NEGATIVE:")
    print("-" * 40)
    for _, combo in combinazioni_piu_negative.iterrows():
        print(f"   > r/{combo['nazione']} - {combo['tema']}: {combo['polarita_media']:.3f} ({combo['commenti']} commenti)")  # AGGIUNTO INFO
    
    
    # 4. ANALISI POLARIZZAZIONE
    print("-" * 40)
    print("4. ANALISI POLARIZZAZIONE NAZIONALE")
    print("-" * 40)
    
    polarizzazione_per_nazione = {}
    
    for nazione in df_sentiment['subreddit'].unique():
        df_nazione = df_sentiment[df_sentiment['subreddit'] == nazione]
        
        # Calcola vari indicatori di polarizzazione
        varianza_polarita = df_nazione['polarita'].var()
        percentuale_estremi = ((df_nazione['polarita'] > 0.3) | (df_nazione['polarita'] < -0.3)).mean() * 100
        indice_polarizzazione = varianza_polarita * percentuale_estremi / 100
        
        polarizzazione_per_nazione[nazione] = {
            'varianza_polarita': varianza_polarita,
            'percentuale_estremi': percentuale_estremi,
            'indice_polarizzazione': indice_polarizzazione,
            'commenti_analizzati': len(df_nazione)
        }
    
    # Classifica per polarizzazione
    nazioni_polarizzate = sorted(polarizzazione_per_nazione.items(), 
                                key=lambda x: x[1]['indice_polarizzazione'], 
                                reverse=True)
    
    print("Nazioni più polarizzate (alta varianza + molti commenti estremi):")
    for nazione, stats in nazioni_polarizzate[:5]:
        print(f"   >< r/{nazione}: indice={stats['indice_polarizzazione']:.3f}, "
              f"estremi={stats['percentuale_estremi']:.1f}%")
    
    return sentiment_per_nazione, df_sentiment_temi, polarizzazione_per_nazione
