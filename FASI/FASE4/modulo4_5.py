import pandas as pd  
from textblob import TextBlob

def analisi_correlazioni_tematiche_sentiment(df_sentiment):
    """
    Analizza correlazioni tra temi e sentiment
    """
    ##########################################df_sentiment HA I VALORI RELATIVI AI TEMI
    print("\n")
    print("="*50, "> ANALISI DELLA CORRELAZIONI TRA TEMATICHE E SENTIMENT ... (modulo 4_5) ")

    
    colonne_temi = [col for col in df_sentiment.columns if col.startswith('tema_')]
    #print(colonne_temi)
    #print(f"--> Colonne: {list(df_sentiment.columns)}")

    if not colonne_temi:
        print("---------> MANCA LA COLONNA CON I TEMI <---------- ")
        print("   Colonne disponibili:", list(df_sentiment.columns))
        return {}, [], pd.DataFrame()

    
    # Calcola sentiment per commento (se non già presente)
    if 'sentiment' not in df_sentiment.columns:
        print("Calcolo sentiment per commenti...")
        df_sentiment['sentiment'] = df_sentiment['comment_text'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity if isinstance(x, str) and len(x) > 10 else 0
        )
    
    # 1. SENTIMENT MEDIO PER TEMA
    print("-" * 40)
    print("1. SENTIMENT MEDIO PER TEMA:")
    print("-" * 40)

    sentiment_per_tema = {}
    colonne_temi = [col for col in df_sentiment.columns if col.startswith('tema_')]
    
    for colonna_tema in colonne_temi:
        tema = colonna_tema.replace('tema_', '')
        sentiment_medio = df_sentiment[df_sentiment[colonna_tema] == 1]['sentiment'].mean()
        sentiment_per_tema[tema] = sentiment_medio
    
    # Ordina per sentiment
    temi_ordinati_sentiment = sorted(sentiment_per_tema.items(), key=lambda x: x[1], reverse=True)
    
    print("--> Temi ordinati per sentiment (da più positivo a più negativo):")
    print("-" * 40)
    for tema, sentiment in temi_ordinati_sentiment:
        print(f"   • {tema}: {sentiment:.3f}")
    
    # 2. SENTIMENT PER TEMA E NAZIONE
    print("-" * 40)
    print("2. SENTIMENT PER COPPIA TEMA-NAZIONE (Top 5):")
    print("-" * 40)
    combinazioni_significative = []
    
    for colonna_tema in colonne_temi:
        tema = colonna_tema.replace('tema_', '')
        
        for nazione in df_sentiment['subreddit'].unique():
            df_filtro = df_sentiment[(df_sentiment[colonna_tema] == 1) & 
                                  (df_sentiment['subreddit'] == nazione)]
            
            if len(df_filtro) >= 5:  # Almeno 5 commenti per statistica
                sentiment_medio = df_filtro['sentiment'].mean()
                combinazioni_significative.append({
                    'tema': tema,
                    'nazione': nazione,
                    'sentiment': sentiment_medio,
                    'commenti': len(df_filtro)
                })
    
    # Top 5 più positive e negative
    combinazioni_ordinate = sorted(combinazioni_significative, key=lambda x: x['sentiment'])
    
    print("Combinazioni più NEGATIVE:")
    print("-" * 40)
    for combo in combinazioni_ordinate[:5]:
        print(f"   • r/{combo['nazione']} - {combo['tema']}: {combo['sentiment']:.3f} ({combo['commenti']} commenti)")
    
    print("\nCombinazioni più POSITIVE:")
    print("-" * 40)
    for combo in combinazioni_ordinate[-5:]:
        print(f"   • r/{combo['nazione']} - {combo['tema']}: {combo['sentiment']:.3f} ({combo['commenti']} commenti)")
    
    # 3. MATRICE DI CORRELAZIONE TEMI
    print("-" * 40)
    print("3. CREAZIONE MATRICE DI CORRELAZIONE TRA TEMI:")
    print("-" * 40)
    # Crea matrice di co-occorrenza temi
    matrice_correlazione = pd.DataFrame()
    
    for col1 in colonne_temi:
        correlazioni = []
        for col2 in colonne_temi:
            correlazione = df_sentiment[col1].corr(df_sentiment[col2])
            correlazioni.append(correlazione)
        matrice_correlazione[col1] = correlazioni
    
    matrice_correlazione.index = [col.replace('tema_', '') for col in colonne_temi]
    matrice_correlazione.columns = [col.replace('tema_', '') for col in colonne_temi]
    
    # Trova correlazioni forti (|r| > 0.1)
    correlazioni_forti = []
    for i, tema1 in enumerate(matrice_correlazione.index):
        for j, tema2 in enumerate(matrice_correlazione.columns):
            if i < j:  # Evita duplicati
                correlazione = matrice_correlazione.iloc[i, j]
                if abs(correlazione) > 0.1:
                    correlazioni_forti.append((tema1, tema2, correlazione))
    
    correlazioni_forti.sort(key=lambda x: abs(x[2]), reverse=True)
    
    print("Correlazioni tematiche più forti:")
    print("-" * 40)
    for tema1, tema2, corr in correlazioni_forti[:10]:
        print(f"   • {tema1} ↔ {tema2}: {corr:.3f}")
    
    return sentiment_per_tema, combinazioni_significative, matrice_correlazione