from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def analisi_cluster_nazioni(metriche_nazioni):
    """
    Crea cluster di nazioni basati su similarità di volume commenti e engagement ratio
    """
    print("\n")
    print("="*50, "> CLUSTERING NAZIONI PER SIMILARITÀ...")
    
    # Seleziona solo le 2 feature principali
    features = metriche_nazioni[[
        'commenti_totali', 
        'engagement_ratio'
    ]]
        
    # Standardizzazione
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
        
    # Sostituisci il loop con:
    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(features_scaled)

    metriche_nazioni['cluster'] = clusters
    
    # Assegna nomi semplici ai cluster
    nomi_cluster = {}
    for i in range(n_clusters):
        nomi_cluster[i] = f"CLUSTER {i+1}"
    
    metriche_nazioni['tipo_comunita'] = metriche_nazioni['cluster'].map(nomi_cluster)
    
    # Analizza ogni cluster
    print("\n" + "="*60)
    print("CLUSTER TROVATI:")
    print("="*60)
    
    for cluster_num in range(n_clusters):
        nazioni_cluster = metriche_nazioni[metriche_nazioni['cluster'] == cluster_num].index.tolist()
        cluster_data = metriche_nazioni[metriche_nazioni['cluster'] == cluster_num]
        
        # Statistiche del cluster
        avg_commenti = cluster_data['commenti_totali'].mean()
        avg_engagement = cluster_data['engagement_ratio'].mean()
        std_commenti = cluster_data['commenti_totali'].std()
        std_engagement = cluster_data['engagement_ratio'].std()
        
        print(f"\n--> {nomi_cluster[cluster_num].upper()}:")
        print(f"   > Volume: {avg_commenti:,.0f} ± {std_commenti:,.0f} commenti")
        print(f"   > Engagement: {avg_engagement:.2f} ± {std_engagement:.2f}")
        print(f"   > Nazioni ({len(nazioni_cluster)}):")
        
        for nazione in nazioni_cluster:
            commenti = metriche_nazioni.loc[nazione, 'commenti_totali']
            engagement = metriche_nazioni.loc[nazione, 'engagement_ratio']
            print(f"      > r/{nazione} ({commenti:,} commenti, engagement: {engagement:.2f})")
    
    # Visualizza la distribuzione
    print("\n" + "="*60)
    print("DISTRIBUZIONE CLUSTER:")
    print("="*60)
    
    distribuzione = metriche_nazioni['tipo_comunita'].value_counts()
    for cluster, count in distribuzione.items():
        cluster_data = metriche_nazioni[metriche_nazioni['tipo_comunita'] == cluster]
        avg_c = cluster_data['commenti_totali'].mean()
        avg_e = cluster_data['engagement_ratio'].mean()
        print(f"   {cluster}: {count} nazioni - {avg_c:,.0f} commenti, engagement {avg_e:.2f}")
    
    return metriche_nazioni