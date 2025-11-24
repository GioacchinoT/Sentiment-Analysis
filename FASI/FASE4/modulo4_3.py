import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def crea_visualizzazioni_sentiment(sentiment_per_nazione, df_sentiment_temi, polarizzazione_per_nazione, df_sentiment):
    """
    Crea visualizzazioni avanzate per l'analisi di sentiment
    """
    print("\n")
    print("="*50, ">  CREAZIONE VISUALIZZAZIONI SENTIMENT AVANZATE ... (modulo 4_3) ")
    
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # Configurazione figura
    fig = plt.figure(figsize=(22, 18))
    
    # 1. MAPPA TERMICA SENTIMENT PER NAZIONE
    plt.subplot(3, 3, 1)
    
    # Prepara dati per heatmap
    heatmap_data = sentiment_per_nazione[['polarita_media', 'soggettivita_media', 'percentuale_positivi']]
    heatmap_data_normalized = (heatmap_data - heatmap_data.mean()) / heatmap_data.std()
    
    sns.heatmap(heatmap_data_normalized, 
                annot=heatmap_data.round(3),
                fmt='.3f',
                cmap='RdYlBu_r',
                center=0,
                linewidths=0.5,
                cbar_kws={'label': 'Deviazioni Standard'})
    
    plt.title('Mappa Sentiment per Nazione\n(Polarità, Soggettività, % Positivi)', 
              fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    # 2. DISTRIBUZIONE SENTIMENT GLOBALE
    plt.subplot(3, 3, 2)
    
    # Istogramma polarità
    plt.hist(df_sentiment['polarita'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(x=df_sentiment['polarita'].mean(), color='red', linestyle='--', 
                label=f'Media: {df_sentiment["polarita"].mean():.3f}')
    plt.xlabel('Polarità del Sentiment')
    plt.ylabel('Frequenza')
    plt.title('Distribuzione Globale della Polarità', fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig('report e grafici generati/analisi_sentiment_comparata.png', dpi=300, bbox_inches='tight')
    print(" ----------------->   Visualizzazione salvata: report e grafici generati/analisi_sentiment_comparata.png")

    crea_distribuzione_polarizzazione_per_nazione(df_sentiment, sentiment_per_nazione, polarizzazione_per_nazione)
    
    return fig


#################################################################################################################################################
#####                                            GRAFICO POLARIZZAZIONE                                                                      #####
#################################################################################################################################################

def crea_distribuzione_polarizzazione_per_nazione(df_sentiment, sentiment_per_nazione, polarizzazione_per_nazione):
    """
    Crea un grafico separato e più dettagliato sulla distribuzione della polarizzazione
    """
    print("\n")
    print("="*50, "CREAZIONE GRAFICO DISTRIBUZIONE POLARIZZAZIONE...")
    
    fig, ((ax2)) = plt.subplots(1, 1, figsize=(20, 12))
    nazioni_ordinate = sentiment_per_nazione.sort_values('polarita_media', ascending=False).index

    
    # 2. DENSITÀ DEI VALORI ESTREMI
    for i, nazione in enumerate(nazioni_ordinate):
        df_nazione = df_sentiment[df_sentiment['subreddit'] == nazione]
        estremi_pos = (df_nazione['polarita'] > 0.3).sum()
        estremi_neg = (df_nazione['polarita'] < -0.3).sum()
        total_estremi = estremi_pos + estremi_neg
        
        ax2.bar(i, total_estremi, color='coral', alpha=0.7, label='Estremi' if i == 0 else "")
        ax2.bar(i, estremi_pos, color='green', alpha=0.7, label='Positivi Estremi' if i == 0 else "")
    
    ax2.set_xticks(range(len(nazioni_ordinate)))
    ax2.set_xticklabels([f"r/{n}" for n in nazioni_ordinate], rotation=45)
    ax2.set_ylabel('Numero Commenti Estremi')
    ax2.set_title('Commenti con Polarità Estrema (>|0.3|)', fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('report e grafici generati/distribuzione_polarizzazione_dettagliata.png', dpi=300, bbox_inches='tight')
    print("------------> Grafico polarizzazione salvato: report e grafici generati/distribuzione_polarizzazione_dettagliata.png")
    
    return fig