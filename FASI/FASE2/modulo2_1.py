import pandas as pd

#CARICAMENTO DATASET
def carica_dataset():
    print("caricamento dataset...")
    
    file_path = "dataset/ds_fine.csv" 

    try:
        df = pd.read_csv(file_path)
        print(f"--> Dataset caricato: {file_path}")
        print(f"--> Righe: {len(df):,}")
        return df
    except Exception as e:
        print(f"Errore nel caricamento: {e}")
        exit()

#Verifica delle colonne
def setting_preliminare(df):
    colonne_necessarie = ['subreddit', 'comment_text', 'comment_score']
    colonne_mancanti = [col for col in colonne_necessarie if col not in df.columns]

    if colonne_mancanti:
        return colonne_mancanti
    else:
        print(" ---------- Setting preliminare effettuato ------------")


# =============================================================================
# 2. PREPROCESSING E PULIZIA DATI
# =============================================================================

def preprocessing_dati(df):

    print("\n")
    print("-"*50, "> PRE PROCESSING DATI... \n")
    
    # Rinomina le colonne 
    if 'comment_body' in df.columns and 'comment_text' not in df.columns:
        df = df.rename(columns={'comment_body': 'comment_text'})
    
    #  Gestione valori mancanti
    colonne_vuote = [col for col in df.columns if 'text' in col.lower() or 'title' in col.lower() or 'body' in col.lower()]
    for col in colonne_vuote:
        df[col] = df[col].fillna('')
    
    # Rimozione commenti troppo corti
    righe_pre = len(df)
    df = df[df['comment_text'].str.len() > 5]  
    righe_post = len(df)
    print(f"   > Commenti rimossi (troppo corti): {righe_pre - righe_post}")
    
    # Conversione date 
    colonne_data = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower() or 'created' in col.lower()]
    if colonne_data:
        for col in colonne_data:
            try:
                df[col] = pd.to_datetime(df[col])
                print(f"   > Convertita colonna data: {col}")
            except:
                print(f"   > Impossibile convertire: {col}")
    
    # Verifica subreddit
    nazioni = df['subreddit'].unique()
    print(f"   > Nazioni presenti ({len(nazioni)}): {nazioni}")
    
    # 5. Aggiungi colonne utili
    df['comment_length'] = df['comment_text'].str.len()
    df['has_high_engagement'] = df['comment_score'] > df['comment_score'].quantile(0.75) # --> se true vuol dire che il commento è nel top 25% per engagement
    
    print(f" Preprocessing completato: {len(df)} righe")
    return df


def crea_struttura_temporale_reale(df):
    print("CREAZIONE STRUTTURA TEMPORALE CON DATI")
    
    df['data_giorno'] = pd.to_datetime(df['comment_created']).dt.date
    
    # Crea attività giornaliera per nazione
    attivita_giornaliera_reale = df.groupby(['data_giorno', 'subreddit']).size().unstack(fill_value=0)
    
    print(f"-------- Struttura creata: --------")
    print(f"   > Periodo: {attivita_giornaliera_reale.index.min()} - {attivita_giornaliera_reale.index.max()}")
    print(f"   > Giorni: {len(attivita_giornaliera_reale)}")
    print(f"   > Nazioni: {len(attivita_giornaliera_reale.columns)}")
    print(f"   > Commenti totali: {attivita_giornaliera_reale.sum().sum():,}")
    
    return attivita_giornaliera_reale

def analisi_comparativa(df):

    print("\n")
    print("="*50, "> ANALISI COMPARATIVA PRELIMINARE TRA NAZIONI... (modulo 2_1)")

    # 1. METRICHE FONDAMENTALI PER NAZIONE
    print(" "*50, "\n TABELLA METRICHE FONDAMENTALI PER NAZIONE:\n")
    metriche_fondamentali = df.groupby('subreddit').agg({
        'comment_id': ['count', 'nunique'],
        'comment_score': ['sum', 'mean', 'median', 'std', 'max'],
        'post_score': ['mean', 'max'],
        'comment_text': lambda x: x.str.len().mean() # --> calcolo della lunghezza media dei commenti per ogni nazione
    }).round(2)

    # Rinomina colonne 
    metriche_fondamentali.columns = [
        'commenti_totali', 'commenti_unici',
        'upvotes_totali', 'upvote_medio', 'upvote_mediano', 'upvote_devstd', 'upvote_max',
        'post_score_medio', 'post_score_max',
        'lunghezza_media_caratteri'
    ]

    # Calcola metriche aggiuntive
    metriche_fondamentali['engagement_ratio'] = (metriche_fondamentali['upvotes_totali'] / metriche_fondamentali['commenti_totali']).round(2)
    metriche_fondamentali['commenti_per_post'] = (metriche_fondamentali['commenti_totali'] / df.groupby('subreddit')['post_title'].nunique()).round(1)

    # stampa della tabella 
    print("METRICHE COMPLETE:")
    print("-" * 120)
    with pd.option_context('display.max_columns', None, 'display.width', 1000):
        print(metriche_fondamentali)
    print("-" * 120)
    
    # 2. CLASSIFICA NAZIONI PER CATEGORIE
    print("\n")
    print(" "*50, "CLASSIFICHE NAZIONALI (top 5)")
    
    
    classifiche = {
        'VOLUME COMMENTI': metriche_fondamentali.nlargest(5, 'commenti_totali')[['commenti_totali']],
        'ENGAGEMENT RATIO': metriche_fondamentali.nlargest(5, 'engagement_ratio')[['engagement_ratio']],
        'UPVOTE MEDIO': metriche_fondamentali.nlargest(5, 'upvote_medio')[['upvote_medio']],
        'COMMENTO PIU  VIRALE': metriche_fondamentali.nlargest(5, 'upvote_max')[['upvote_max']],
        'LUNGHEZZA COMMENTI': metriche_fondamentali.nlargest(5, 'lunghezza_media_caratteri')[['lunghezza_media_caratteri']]
    }
    
    for categoria, classifica in classifiche.items():
        print(f"\n ---->  {categoria}:")
        for nazione, stats in classifica.iterrows():
            valore = stats[0]
            print(f"   • r/{nazione}: {valore}")
    

    # ANALISI TOP POST PER NAZIONE

    print("\n  TOP POST PER NAZIONE")
    print("-" * 50)
    
    top_post_per_nazione = df.groupby(['subreddit', 'post_title']).agg({
        'comment_id': 'count',
        'comment_score': 'sum'
    }).nlargest(10, 'comment_score')
    
    top_post_per_nazione.columns = ['commenti_totali', 'engagement_totale']
    print("Post più discussi per engagement:")
    print(top_post_per_nazione)

    print("-"*40)
    print("----> RAPPORTO COMMENTI / POST PER NAZIONE")
    print("-"*40)

    nazioni_ordinate = metriche_fondamentali.sort_values('commenti_per_post', ascending=False)

    for nazione, stats in nazioni_ordinate.iterrows():
        commenti_totali = stats['commenti_totali']
        post_totali = stats['post_totali'] if 'post_totali' in stats else df.groupby('subreddit')['post_title'].nunique()[nazione]
        rapporto = stats['commenti_per_post']
        
        print(f"• r/{nazione}:")
        print(f"              {commenti_totali} commenti / {post_totali} post = {rapporto:.1f} commenti per post")
    
    return metriche_fondamentali
