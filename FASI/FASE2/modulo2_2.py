import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def crea_visualizzazioni_comparative(metriche_nazioni, df):
    """
    Crea visualizzazioni comparative tra tutte le nazioni
    """
    print("\n")
    print("="*50, "> CREAZIONE VISUALIZZAZION COMPARATIVE... (modulo 2_2)")

    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # Configurazione subplot
    fig = plt.figure(figsize=(20, 15))
    
    # 1. HEATMAP METRICHE PRINCIPALI
    plt.subplot(2, 3, 1)
    metriche_heatmap = metriche_nazioni[['commenti_totali', 'upvote_medio', 'engagement_ratio', 'lunghezza_media_caratteri']]
    metriche_heatmap_normalized = (metriche_heatmap - metriche_heatmap.mean()) / metriche_heatmap.std()
    
    sns.heatmap(metriche_heatmap_normalized, 
                annot=metriche_heatmap.round(1), 
                cmap='RdYlGn', 
                center=0,
                fmt='.1f',
                linewidths=0.5)
    plt.title('Heatmap Metriche Principali per Nazione\n(Valori standardizzati)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    # 2. BAR CHART - TOP 10 NAZIONI PER ENGAGEMENT
    plt.subplot(2, 3, 2)
    top_10_engagement = metriche_nazioni.nlargest(10, 'engagement_ratio')['engagement_ratio']
    bars = plt.barh(range(len(top_10_engagement)), top_10_engagement.values, color='lightcoral')
    plt.yticks(range(len(top_10_engagement)), [f"r/{sub}" for sub in top_10_engagement.index])
    plt.xlabel('Engagement Ratio (Upvotes/Commento)')
    plt.title('Top 10 Nazioni per Engagement', fontweight='bold')
    
    # Aggiungi valori sulle barre
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{bar.get_width():.2f}', ha='left', va='center')
    
    # 3. SCATTER PLOT - VOLUME vs ENGAGEMENT
    plt.subplot(2, 3, 3)
    plt.scatter(metriche_nazioni['commenti_totali'], 
                metriche_nazioni['engagement_ratio'], 
                s=metriche_nazioni['upvote_max']/10,  # Dimensione punti basata su commento più virale
                alpha=0.6, 
                c=metriche_nazioni['upvote_medio'],
                cmap='viridis')
    
    plt.xlabel('Volume Commenti')
    plt.ylabel('Engagement Ratio')
    plt.title('Volume vs Engagement per Nazione\n(Dimensione = Commento più virale)', fontweight='bold')
    plt.colorbar(label='Upvote Medio')
    
    # Aggiungi etichette nazioni
    for nazione in metriche_nazioni.index:
        plt.annotate(f"r/{nazione}", 
                    (metriche_nazioni.loc[nazione, 'commenti_totali'], 
                     metriche_nazioni.loc[nazione, 'engagement_ratio']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # 4. BOX PLOT - DISTRIBUZIONE UPVOTES PER NAZIONE
    plt.subplot(2, 3, 4)
    # Prendi solo le prime 8 nazioni per chiarezza
    top_8_nazioni = metriche_nazioni.nlargest(8, 'commenti_totali').index
    df_top_8 = df[df['subreddit'].isin(top_8_nazioni)]
    
    sns.boxplot(data=df_top_8, x='subreddit', y='comment_score')
    plt.xticks(rotation=45)
    plt.title('Distribuzione Upvotes per Nazione (Top 8)', fontweight='bold')
    plt.ylabel('Upvotes per Commento')
    plt.xlabel('')
    

    # 6. RADAR CHART - PROFILO NAZIONALE
    plt.subplot(2, 3, 6)
    # Seleziona 3 nazioni rappresentative
    nazioni_rappresentative = [
        metriche_nazioni.nlargest(1, 'commenti_totali').index[0],  # Più attiva
        metriche_nazioni.nlargest(1, 'engagement_ratio').index[0],  # Miglior engagement
        metriche_nazioni.nlargest(1, 'upvote_max').index[0]  # Più virale
    ]
    
    # Metriche per radar chart
    metriche_radar = ['commenti_totali', 'upvote_medio', 'engagement_ratio', 'lunghezza_media_caratteri']
    metriche_normalizzate = metriche_nazioni[metriche_radar].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    angles = np.linspace(0, 2*np.pi, len(metriche_radar), endpoint=False).tolist()
    angles += angles[:1]  # Chiudi il cerchio
    
    for nazione in nazioni_rappresentative:
        valori = metriche_normalizzate.loc[nazione].tolist()
        valori += valori[:1]  # Chiudi il cerchio
        plt.polar(angles, valori, 'o-', linewidth=2, label=f'r/{nazione}')
    
    plt.xticks(angles[:-1], metriche_radar)
    plt.title('Profilo Comparative 3 Nazioni Rappresentative', fontweight='bold')
    plt.legend(bbox_to_anchor=(1.2, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('report e grafici generati/analisi_comparativa_nazioni.png', dpi=300, bbox_inches='tight')
    print("Grafici salvati ----------->  report e grafici generati/analisi_comparativa_nazioni.png")
    
    return fig
