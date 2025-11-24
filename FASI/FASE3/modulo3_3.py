
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def crea_visualizzazioni_tematiche(df_profilo_tematico, distribuzione_globale, df_tematico):
    """
    Crea visualizzazioni avanzate per l'analisi tematica
    """
    print("\n")
    print("="*50, "> ANALISI CLUSTER E SEGMENTAZIONE NAZIONI... (modulo 3_3)\n")
    
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # Configurazione figura
    fig = plt.figure(figsize=(20, 16))
    
    # 1. HEATMAP TEMI PER NAZIONE
    plt.subplot(2, 2, 1)
    
    # Prepara dati per heatmap
    heatmap_data = df_profilo_tematico.T
    
    sns.heatmap(heatmap_data, 
                annot=True, 
                fmt='.1f', 
                cmap='YlOrRd',
                cbar_kws={'label': 'Percentuale Commenti (%)'},
                linewidths=0.5)
    plt.title('Distribuzione Temi per Nazione (% Commenti)\n', fontsize=14, fontweight='bold')
    plt.xlabel('Nazione')
    plt.ylabel('Tema')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    # 2. BAR CHART - TEMI GLOBALI
    plt.subplot(2, 2, 2)
    
    temi_globali_ordinati = sorted([(tema, stats['conteggio']) 
                                   for tema, stats in distribuzione_globale.items()], 
                                  key=lambda x: x[1], reverse=True)
    
    temi_nomi = [t[0] for t in temi_globali_ordinati]
    temi_conteggi = [t[1] for t in temi_globali_ordinati]
    
    bars = plt.barh(range(len(temi_nomi)), temi_conteggi, color='steelblue')
    plt.yticks(range(len(temi_nomi)), [t.replace('_', ' ').title() for t in temi_nomi])
    plt.xlabel('Numero Commenti')
    plt.title('Distribuzione Globale dei Temi', fontweight='bold')
    
    # Aggiungi percentuali
    for i, bar in enumerate(bars):
        percentuale = (temi_conteggi[i] / len(df_tematico)) * 100
        plt.text(bar.get_width() + max(temi_conteggi)*0.01, bar.get_y() + bar.get_height()/2,
                f'{percentuale:.1f}%', ha='left', va='center', fontsize=9)
    
   
    plt.tight_layout()
    plt.savefig('report e grafici generati/analisi_tematiche_transnazionali.png', dpi=300, bbox_inches='tight')
    print("Visualizzazione salvata: report e grafici generati/analisi_tematiche_transnazionali.png")
    
    return fig
