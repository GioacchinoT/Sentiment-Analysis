from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm
import numpy as np

def analisi_trend_predittiva(andamento_giornaliero, evoluzione_nazionale):
    """
    Analisi predittiva e identificazione trend futuri
    """

    print("\n")
    print("="*50, "> ANALISI TREND PREDITTIVA (modulo 5_4)")
    
    print("-" *40)
    print("   1. TREND GLOBALE")
    print("-" *40)
    
    # Prepara dati per regressione
    x_globale = np.arange(len(andamento_giornaliero)).reshape(-1, 1)
    y_volume_globale = andamento_giornaliero['volume_commenti'].values
    y_sentiment_globale = andamento_giornaliero['sentiment_medio'].values
    
    # Regressione volume
    reg_volume = LinearRegression()
    reg_volume.fit(x_globale, y_volume_globale)
    trend_volume_globale = reg_volume.coef_[0]
    r2_volume = r2_score(y_volume_globale, reg_volume.predict(x_globale))
    
    # Regressione sentiment
    reg_sentiment = LinearRegression()
    reg_sentiment.fit(x_globale, y_sentiment_globale)
    trend_sentiment_globale = reg_sentiment.coef_[0]
    r2_sentiment = r2_score(y_sentiment_globale, reg_sentiment.predict(x_globale))
    
    
    print(f"Trend volume globale: {trend_volume_globale:+.2f} commenti/giorno (R²={r2_volume:.3f})")
    print("-" *40)
    print(f"Trend sentiment globale: {trend_sentiment_globale:+.4f} sentiment/giorno (R²={r2_sentiment:.3f})")
    print("-" *40)
    
    # 2. PROIEZIONI FUTURE
    print("-" *40)
    print(" 2. PROIEZIONI FUTURE (7 GIORNI)")
    print("-" *40)
    
    # Estendi timeline per proiezione
    giorni_futuri = 7
    x_futuro = np.arange(len(andamento_giornaliero), len(andamento_giornaliero) + giorni_futuri).reshape(-1, 1)
    
    volume_proiettato = reg_volume.predict(x_futuro)
    sentiment_proiettato = reg_sentiment.predict(x_futuro)
    
    print("Proiezioni volume commenti:")
    print("-" *40)
    for i, volume in enumerate(volume_proiettato):
        print(f"   > Giorno {i+1}: {volume:.1f} commenti")
    
    print("\nProiezioni sentiment medio:")
    print("-" *40)
    for i, sentiment in enumerate(sentiment_proiettato):
        print(f"   > Giorno {i+1}: {sentiment:.3f}")
    
    
    # 3. SEGNALI DI CAMBIO TREND
    print("-" *40)
    print("  4. SEGNALI DI CAMBIO TREND")
    print("-" *40)
    
    # Usa differenze per identificare cambiamenti
    differenze_volume = andamento_giornaliero['volume_commenti'].diff()
    differenze_sentiment = andamento_giornaliero['sentiment_medio'].diff()
    
    # Soglie per cambiamenti significativi
    soglia_volume = differenze_volume.std() * 1.5
    soglia_sentiment = differenze_sentiment.std() * 2
    
    cambiamenti_volume = differenze_volume[abs(differenze_volume) > soglia_volume]
    cambiamenti_sentiment = differenze_sentiment[abs(differenze_sentiment) > soglia_sentiment]
    
    print(f"Cambiamenti significativi di VOLUME identificati: {len(cambiamenti_volume)}")
    print("-" *40)
    for data, cambio in cambiamenti_volume.nlargest(3).items():
        print(f"   > {data}: +{cambio:.1f} commenti")
    
    for data, cambio in cambiamenti_sentiment.nlargest(3).items():
        print(f"   > {data}: {cambio:+.3f} sentiment")
    
    return {
        'trend_volume_globale': trend_volume_globale,
        'trend_sentiment_globale': trend_sentiment_globale,
        'proiezioni_volume': volume_proiettato,
        'proiezioni_sentiment': sentiment_proiettato,
        'cambiamenti_significativi': {
            'volume': cambiamenti_volume,
            'sentiment': cambiamenti_sentiment
        }
    }
 