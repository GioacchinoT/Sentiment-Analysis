import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def setup_analisi_temporale(df_sentiment):
    """
    Prepara il dataset per l'analisi temporale usando comment_created
    """
    print("\n")
    print("="*50, "> CONFIGURAZIONE FASE 5... (modulo 5_1)")
    
    # 1. USA SOLO comment_created COME DATA DI RIFERIMENTO
    if 'comment_created' not in df_sentiment.columns:
        print("colonna 'comment_created' non trovata")
        return None
    
    # Conversione comment_created in datetime
    df_temp = df_sentiment.copy()
    df_temp['data_datetime'] = pd.to_datetime(df_temp['comment_created'])
    
    # 2. ESTRAZIONE COMPONENTI TEMPORALI
    df_temp['data_giorno'] = df_temp['data_datetime'].dt.date
    df_temp['giorno_settimana'] = df_temp['data_datetime'].dt.day_name()
    df_temp['ora_giorno'] = df_temp['data_datetime'].dt.hour
    df_temp['settimana_anno'] = df_temp['data_datetime'].dt.isocalendar().week
    df_temp['mese_anno'] = df_temp['data_datetime'].dt.to_period('M')
    
    # Creazione periodi temporali
    df_temp['periodo_giornaliero'] = pd.cut(df_temp['ora_giorno'], 
                                          bins=[0, 6, 12, 18, 24], 
                                          labels=['Notte', 'Mattina', 'Pomeriggio', 'Sera'],
                                          include_lowest=True)
    
    # 3. STATISTICHE TEMPORALI
    data_min = df_temp['data_datetime'].min()
    data_max = df_temp['data_datetime'].max()
    range_temporale = data_max - data_min
    giorni_analizzati = range_temporale.days + 1
    
    print(f"--> DATASET TEMPORALE CORRETTO:")
    print(f"   > Periodo commenti: {data_min} - {data_max}")
    print(f"   > Giorni totali: {giorni_analizzati}")
    print(f"   > Commenti totali: {len(df_temp):,}")
    print(f"   > Commenti/giorno (media): {len(df_temp) / giorni_analizzati:.1f}")
    
    # 4. ANALISI DISTRIBUZIONE TEMPORALE
    distribuzione_giornaliera = df_temp['data_giorno'].value_counts()
    print(f" DISTRIBUZIONE GIORNALIERA:")
    print(f"   > Giorno più attivo: {distribuzione_giornaliera.idxmax()} ({distribuzione_giornaliera.max()} commenti)")
    print(f"   > Giorno meno attivo: {distribuzione_giornaliera.idxmin()} ({distribuzione_giornaliera.min()} commenti)")
    
    # Distribuzione mensile
    distribuzione_mensile = df_temp['mese_anno'].value_counts().sort_index()
    print(f"   > Distribuzione mensile:")
    for mese, conteggio in distribuzione_mensile.items():
        print(f"      {mese}: {conteggio} commenti")
    
    return df_temp

