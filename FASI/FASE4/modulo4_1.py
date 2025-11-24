from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

def analizza_sentiment(testo):
    """
    Analizza sentiment per testo inglese
    """
    if not isinstance(testo, str) or len(testo.strip()) < 10:
        return 0.0, 0.0, 'neutro', 'en'
    
    try:
        blob = TextBlob(testo.strip())
        polarita = blob.sentiment.polarity
        soggettivita = blob.sentiment.subjectivity
        
        if polarita > 0.1:
            categoria = 'positivo'
        elif polarita < -0.1:
            categoria = 'negativo'
        else:
            categoria = 'neutro'
            
        return polarita, soggettivita, categoria, 'en'
        
    except Exception as e:
        print(f"Errore analisi sentiment: {e}")
        return 0.0, 0.0, 'neutro', 'en'

def applica_sentiment(df):
    """
    APPLICAZIONE sentiment al dataste

    """
    print("\n")
    print("="*50, ">  APPLICAZIONE SENTIMENT ANALYSIS ... (modulo 4_1) ")
    
    
    risultati_sentiment = []
    
    for idx, row in df.iterrows():
        testo = row['comment_text']
        
        polarita, soggettivita, categoria, lingua_usata = analizza_sentiment(testo)
        
        risultati_sentiment.append({
            'polarita': polarita,
            'soggettivita': soggettivita, 
            'categoria_sentiment': categoria,
            'lingua_analisi': lingua_usata,
            'lingua_target': 'en'  # Tutti in inglese
        })
    
    # Aggiungi colonne al DataFrame
    df_sentiment = df.copy()
    for key in risultati_sentiment[0].keys():
        df_sentiment[key] = [r[key] for r in risultati_sentiment]
    
    # Statistiche
    totale_commenti = len(df_sentiment)
    
    print(f"--> ANALISI COMPLETATA:")
    print("-" * 40)
    print(f"   > Commenti analizzati: {totale_commenti:,}")
    print(f"   > Distribuzione sentiment:")
    
    distribuzione_categorie = df_sentiment['categoria_sentiment'].value_counts() # categorie --> neutro/negativo/positivo
    for categoria, conteggio in distribuzione_categorie.items():
        percentuale = (conteggio / totale_commenti) * 100
        print(f"      > {categoria}: {conteggio:,} commenti ({percentuale:.1f}%)")
    
    print(f"   > Polarità media: {df_sentiment['polarita'].mean():.3f}")
    print(f"   > Soggettività media: {df_sentiment['soggettivita'].mean():.3f}")
    
    return df_sentiment
