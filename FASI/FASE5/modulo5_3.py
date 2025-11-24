import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import os


def crea_visualizzazioni_temporali_avanzate(andamento_giornaliero, evoluzione_nazionale, eventi_significativi, pattern_giornaliero, pattern_settimanale, df_temporale):
    """
    Crea visualizzazioni avanzate per l'analisi temporale
    """
    print("\n")
    print("="*50, "> CREAZIONE VISUALIZZAZIONI TEMPORALI (modulo 5_3)")
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # Configurazione figura principale
    fig = plt.figure(figsize=(24, 20))
    
    # 1. TIMELINE COMPARATA - VOLUME E SENTIMENT
    plt.subplot(3, 3, 1)
    
    # Doppio asse per volume e sentiment
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    # Volume commenti
    line_volume = ax1.plot(andamento_giornaliero.index, andamento_giornaliero['volume_commenti'], 
                          color='blue', alpha=0.7, linewidth=2, label='Volume Commenti')
    ax1.fill_between(andamento_giornaliero.index, 0, andamento_giornaliero['volume_commenti'], 
                    alpha=0.3, color='blue')
    
    # Media mobile volume
    ax1.plot(andamento_giornaliero.index, andamento_giornaliero['volume_rolling_7d'], 
            color='darkblue', linewidth=3, label='Media Mobile 7gg')
    
    # Sentiment
    line_sentiment = ax2.plot(andamento_giornaliero.index, andamento_giornaliero['sentiment_medio'], 
                             color='red', linewidth=2, label='Sentiment Medio')
    
    # Media mobile sentiment
    ax2.plot(andamento_giornaliero.index, andamento_giornaliero['sentiment_rolling_7d'], 
            color='darkred', linewidth=2, linestyle='--', label='Sentiment Media Mobile')
    
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Volume Commenti', color='blue')
    ax2.set_ylabel('Sentiment Medio', color='red')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Linea zero per sentiment
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    # Combina leggende
    lines = line_volume + line_sentiment
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.title('Timeline Comparata: Volume e Sentiment delle Discussioni', 
              fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    
    # 2. EVOLUZIONE NAZIONI TOP 6
    plt.subplot(3, 3, 2)
    
    # Seleziona 6 nazioni più attive
    nazioni_top_6 = sorted(evoluzione_nazionale.items(), 
                          key=lambda x: x[1]['volume_medio'], reverse=True)[:6]
    
    for nazione, stats in nazioni_top_6:
        andamento = stats['andamento']
        plt.plot(andamento.index, andamento['volume'], 
                linewidth=2, label=f'r/{nazione}', alpha=0.8)
    
    plt.xlabel('Data')
    plt.ylabel('Volume Commenti')
    plt.title('Evoluzione Volume per Nazioni Top 6', fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    
    # 3. MAPPA TERMICA EVOLUZIONE NAZIONALE
    plt.subplot(3, 3, 3)
    
    # Prepara dati per heatmap
    heatmap_data = []
    nazioni_heatmap = [n for n, _ in nazioni_top_6]
    dates_heatmap = sorted(df_temporale['data_giorno'].unique())
    
    for nazione in nazioni_heatmap:
        if nazione in evoluzione_nazionale:
            andamento = evoluzione_nazionale[nazione]['andamento']
            sentiment_series = andamento.reindex(dates_heatmap)['sentiment'].fillna(0)
            heatmap_data.append(sentiment_series.values)
    
    if heatmap_data:
        heatmap_data = np.array(heatmap_data)
        
        im = plt.imshow(heatmap_data, aspect='auto', cmap='RdYlBu', vmin=-0.3, vmax=0.3)
        plt.colorbar(im, label='Sentiment Medio')
        plt.yticks(range(len(nazioni_heatmap)), [f"r/{n}" for n in nazioni_heatmap])
        
        # Ottimizza etichette date (mostra solo alcune)
        n_dates = len(dates_heatmap)
        step = max(1, n_dates // 10)
        plt.xticks(range(0, n_dates, step), 
                  [str(dates_heatmap[i]) for i in range(0, n_dates, step)], 
                  rotation=45)
        
        plt.title('Mappa Termica Sentiment per Nazioni Top 6', fontweight='bold')
        plt.xlabel('Data')
    
    # 4. PATTERN GIORNALIERO
    plt.subplot(3, 3, 4)
    
    plt.bar(pattern_giornaliero.index, pattern_giornaliero['comment_id'], 
            color='lightblue', edgecolor='darkblue', alpha=0.7)
    plt.xlabel('Ora del Giorno')
    plt.ylabel('Numero Commenti')
    plt.title('Distribuzione Commenti per Ora del Giorno', fontweight='bold')
    plt.grid(alpha=0.3, axis='y')
    
    # Evidenzia ora più attiva
    ora_max = pattern_giornaliero['comment_id'].idxmax()
    plt.axvline(x=ora_max, color='red', linestyle='--', alpha=0.8, 
                label=f'Ora più attiva: {ora_max}:00')
    plt.legend()
    # 5. PATTERN SETTIMANALE
    plt.subplot(3, 3, 5)

    giorni_italiano = {'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mer', 
                    'Thursday': 'Gio', 'Friday': 'Ven', 'Saturday': 'Sab', 'Sunday': 'Dom'}

    pattern_settimanale_index = [giorni_italiano[g] for g in pattern_settimanale.index]

    bars = plt.bar(pattern_settimanale_index, pattern_settimanale['comment_id'], 
                color=['lightgray' if g != pattern_settimanale['comment_id'].idxmax() 
                        else 'orange' for g in pattern_settimanale.index])

    plt.xlabel('Giorno della Settimana')
    plt.ylabel('Numero Commenti')
    plt.title('Distribuzione Commenti per Giorno della Settimana', fontweight='bold')
    plt.grid(alpha=0.3, axis='y')

    # Aggiungi valori sulle barre - CORREZIONE APPLICATA
    for bar in bars:
        height = bar.get_height()
        # Controlla se height è NaN prima di convertire
        if pd.notna(height):  # oppure: if not np.isnan(height):
            plt.text(bar.get_x() + bar.get_width()/2., height + max(pattern_settimanale['comment_id'])*0.01,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')

    # 6. ANALISI EVENTI SIGNIFICATIVI
    plt.subplot(3, 3, 6)
    
    if eventi_significativi:
        # Prepara dati per scatter plot eventi
        dates_events = [e['data'] for e in eventi_significativi]
        volumes_events = [e['volume'] for e in eventi_significativi]
        sentiments_events = [e['sentiment'] for e in eventi_significativi]
        types_events = [e['tipo_evento'] for e in eventi_significativi]
        
        colors = {'volume_anomalo': 'red', 'sentiment_estremo': 'blue'}
        
        for date, volume, sentiment, tipo in zip(dates_events, volumes_events, sentiments_events, types_events):
            plt.scatter(date, volume, c=colors[tipo], s=100, alpha=0.7, label=tipo if tipo not in plt.gca().get_legend_handles_labels()[1] else "")
        
        plt.xlabel('Data')
        plt.ylabel('Volume Commenti')
        plt.title('Eventi Significativi Identificati\n(Rosso=Volume, Blu=Sentiment)', fontweight='bold')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
    
    # 7. CORRELAZIONE TEMPORALE SENTIMENT-ENGAGEMENT
    plt.subplot(3, 3, 7)
    
    # Calcola correlazione giornaliera
    correlazioni_giornaliere = []
    for data in andamento_giornaliero.index:
        df_giorno = df_temporale[df_temporale['data_giorno'] == data]
        if len(df_giorno) > 10:
            correlazione = df_giorno['polarita'].corr(df_giorno['comment_score'])
            correlazioni_giornaliere.append({'data': data, 'correlazione': correlazione})
    
    if correlazioni_giornaliere:
        df_correlazioni = pd.DataFrame(correlazioni_giornaliere).set_index('data')
        plt.plot(df_correlazioni.index, df_correlazioni['correlazione'], 
                marker='o', linewidth=2, color='purple', alpha=0.7)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        plt.xlabel('Data')
        plt.ylabel('Correlazione')
        plt.title('Correlazione Giornaliera Sentiment-Engagement', fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
    
    # 8. COMPARAZIONE ANDAMENTO TEMI NEL TEMPO
    plt.subplot(3, 3, 8)
    
    # Seleziona temi principali
    colonne_temi = [col for col in df_temporale.columns if col.startswith('tema_')]
    temi_principali = []
    
    for colonna in colonne_temi:
        if df_temporale[colonna].sum() > len(df_temporale) * 0.05:  # Almeno 5% dei commenti
            temi_principali.append(colonna)
    
    if len(temi_principali) > 0:
        # Analizza evoluzione temi
        evoluzione_temi = {}
        for colonna in temi_principali[:4]:  # Massimo 4 temi per chiarezza
            tema = colonna.replace('tema_', '')
            evoluzione_tema = df_temporale.groupby('data_giorno')[colonna].mean() * 100
            evoluzione_temi[tema] = evoluzione_tema
        
        for tema, serie in evoluzione_temi.items():
            plt.plot(serie.index, serie.values, linewidth=2, label=tema, alpha=0.8)
        
        plt.xlabel('Data')
        plt.ylabel('Percentuale Commenti (%)')
        plt.title('Evoluzione Temi Principali nel Tempo', fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('report e grafici generati/analisi_temporale_completa.png', dpi=300, bbox_inches='tight')
    print("--->  Visualizzazione salvata: report e grafici generati/analisi_temporale_completa.png")
    
    return fig

#############################################################################################################################################
#####                                                       GRAFICI NAZIONALI                                                           #####
#############################################################################################################################################


def crea_grafici_temi_temporali_per_nazione(df_temporale):
    """
    Crea grafici separati per l'evoluzione dei temi nel tempo per ogni nazione
    """
    print("\n CREAZIONE GRAFICI TEMI TEMPORALI PER NAZIONE...")
    
    nazioni_analizzate = 0
    
    for nazione in df_temporale['subreddit'].unique():
        df_nazione = df_temporale[df_temporale['subreddit'] == nazione]
        
        if len(df_nazione) < 50:  
            continue
        
        # Seleziona colonne tema
        colonne_temi = [col for col in df_nazione.columns if col.startswith('tema_')]
        
        # Calcola evoluzione temi nel tempo
        evoluzione_temi = df_nazione.groupby('data_giorno')[colonne_temi].mean() * 100
        
        # Seleziona solo i top 4 temi per chiarezza
        temi_totali = df_nazione[colonne_temi].sum().sort_values(ascending=False)
        top_temi = temi_totali.head(4).index.tolist()
        
        if len(top_temi) == 0:
            continue
        
        # Crea grafico
        fig, ax = plt.subplots(figsize=(15, 8))
        
        for tema in top_temi:
            tema_nome = tema.replace('tema_', '').replace('_', ' ').title()
            # Media mobile 7 giorni per smoothing
            serie_tema = evoluzione_temi[tema].rolling(window=7, center=True).mean()
            ax.plot(evoluzione_temi.index, serie_tema, 
                   linewidth=2, label=tema_nome, alpha=0.8)
        
        ax.set_title(f'EVOLUZIONE TEMI - r/{nazione}\n(Top 4 Temi - Media Mobile 7gg)', 
                    fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentuale Commenti (%)')
        ax.set_xlabel('Data')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
        
        # Aggiungi statistiche
        stats_text = f"Temi Totali Analizzati: {len(colonne_temi)} | Commenti: {len(df_nazione):,}"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # Salva grafico
        filename = f"TEMATICHE PER TEMPO/temi_timeline_{nazione}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        nazioni_analizzate += 1
        print(f"        ----> Grafico temi salvato: {filename} (IN TEMATICHE PER TEMPO)")
    
    
    return nazioni_analizzate