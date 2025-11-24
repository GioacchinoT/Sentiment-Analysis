from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def analisi_cluster_sentiment(df_sentiment, sentiment_per_nazione):
    print("\n")
    print("="*50, ">  ANALISI CLUSTER DI SENTIMENT... (modulo 4_4) ")
    
    # 1. CLUSTER NAZIONI PER PROFILO SENTIMENT
    print("-" * 40)
    print("1. CLUSTER NAZIONI PER PROFILO SENTIMENT")
    print("-" * 40)
    
    # Features per clustering
    features_clustering = sentiment_per_nazione[['polarita_media', 'soggettivita_media']]
    
    # Standardizzazione
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_clustering)
    
    # Applica K-means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10) 
    clusters = kmeans.fit_predict(features_scaled)
    
    sentiment_per_nazione['cluster_sentiment'] = clusters
    
    nomi_cluster = {}
    
    for cluster_num in range(3):
        cluster_data = sentiment_per_nazione[sentiment_per_nazione['cluster_sentiment'] == cluster_num]
        
        avg_polarita = cluster_data['polarita_media'].mean()
        avg_soggettivita = cluster_data['soggettivita_media'].mean()
        
        # aggiunta info discussioni
        if avg_polarita > 0.06:
            nome = 'Discussioni Positive'
        elif avg_polarita > 0.04:
            nome = 'Discussioni Neutrali'
        else:
            nome = 'Discussioni Leggermente Positive'
        
        # aggiunta info generalità
        if avg_soggettivita > 0.42:
            nome += ' e Soggettive'
        elif avg_soggettivita > 0.38:
            nome += ' e Bilanciate'
        else:
            nome += ' e Oggettive'
        
        nomi_cluster[cluster_num] = nome
    
    sentiment_per_nazione['tipo_discussione'] = sentiment_per_nazione['cluster_sentiment'].map(nomi_cluster)
    
    print("\nComposizione cluster:")
    print("-" * 40)
    for cluster_num in range(3):
        nazioni_cluster = sentiment_per_nazione[sentiment_per_nazione['cluster_sentiment'] == cluster_num].index.tolist()
        print(f"\n   {nomi_cluster[cluster_num].upper()}:")
        for nazione in nazioni_cluster:
            polarita = sentiment_per_nazione.loc[nazione, 'polarita_media']
            soggettivita = sentiment_per_nazione.loc[nazione, 'soggettivita_media']
            print(f"      • r/{nazione} (polarità: {polarita:.3f}, soggettività: {soggettivita:.3f})")

    # 2. ANALISI COMMENTI ESTREMI
    print("-" * 40)
    print("2. ANALISI COMMENTI ESTREMI")
    print("-" * 40)

    commenti_estremamente_positivi = df_sentiment.nlargest(5, 'polarita')[['subreddit', 'comment_text', 'polarita', 'comment_score']]
    commenti_estremamente_negativi = df_sentiment.nsmallest(5, 'polarita')[['subreddit', 'comment_text', 'polarita', 'comment_score']]

    print("Commenti più POSITIVI:")
    print("-" * 40)
    for idx, row in commenti_estremamente_positivi.iterrows():
        print(f"   > r/{row['subreddit']}: {row['polarita']:.3f} ({row['comment_score']} upvotes)")
        print(f"     '{row['comment_text']}'")  
        print()  

    print("\nCommenti più NEGATIVI:")
    print("-" * 40)
    for idx, row in commenti_estremamente_negativi.iterrows():
        print(f"   > r/{row['subreddit']}: {row['polarita']:.3f} ({row['comment_score']} upvotes)")
        print(f"     '{row['comment_text']}'")  
        print()
        
    
    return sentiment_per_nazione
