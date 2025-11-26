import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from adjustText import adjust_text
import warnings
warnings.filterwarnings('ignore')

# ------------------------------------------------------------
# IDENTIFICA PICCHI DI SENTIMENT
# ------------------------------------------------------------
def identifica_picchi_sentiment(andamento_nazione):
    soglia_positiva_assoluta = 0.2
    soglia_negativa_assoluta = -0.2

    picchi_assoluti_pos = andamento_nazione[andamento_nazione['sentiment_medio'] > soglia_positiva_assoluta]
    picchi_assoluti_neg = andamento_nazione[andamento_nazione['sentiment_medio'] < soglia_negativa_assoluta]

    top_estremi_pos = andamento_nazione.nlargest(3, 'sentiment_medio')
    top_estremi_neg = andamento_nazione.nsmallest(3, 'sentiment_medio')

    tutti_picchi = pd.concat([
        picchi_assoluti_pos, 
        picchi_assoluti_neg,
        top_estremi_pos,
        top_estremi_neg
    ]).drop_duplicates()

    return tutti_picchi

def crea_grafici_temporali_con_eventi(df_temporale, andamento_giornaliero, evoluzione_nazionale, eventi_significativi):
    """
    Crea grafici temporali che EVIDENZIANO gli eventi e picchi significativi
    """

    print("\n")
    print("-" * 50, "> CREAZIONE GRAFICI TEMPORALI CON EVIDENZIAZIONE EVENTI...")

    # Crea cartella per i grafici
    cartella_grafici = "grafici_eventi_nazioni"
    if not os.path.exists(cartella_grafici):
        os.makedirs(cartella_grafici)
        print(f"Cartella creata: {cartella_grafici}")

    # Stile grafici
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    nazioni_analizzate = 0

    for nazione in df_temporale['subreddit'].unique():
        df_nazione = df_temporale[df_temporale['subreddit'] == nazione]

        if len(df_nazione) < 10:
            continue

        andamento_nazione = df_nazione.groupby('data_giorno').agg({
            'comment_id': 'count',
            'polarita': ['mean', 'std'],
            'comment_score': 'mean',
            'soggettivita': 'mean'
        }).round(3)

        andamento_nazione.columns = [
            'volume', 'sentiment_medio', 'sentiment_std', 'engagement_medio', 'soggettivita_media'
        ]

        andamento_nazione['volume_rolling_7d'] = andamento_nazione['volume'].rolling(window=7, center=True).mean()
        andamento_nazione['sentiment_rolling_7d'] = andamento_nazione['sentiment_medio'].rolling(window=7, center=True).mean()

        volume_medio = andamento_nazione['volume'].mean()
        volume_std = andamento_nazione['volume'].std()
        picchi_nazione = andamento_nazione[andamento_nazione['volume'] > volume_medio + volume_std]

        fig = plt.figure(figsize=(18, 15))
        gs = fig.add_gridspec(4, 1, height_ratios=[3, 2, 2, 1])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        #ax4 = fig.add_subplot(gs[3])

        # 1️ VOLUME CON EVENTI
        ax1.fill_between(andamento_nazione.index, 0, andamento_nazione['volume'],
                         alpha=0.2, color='blue', label='Volume Giornaliero')
        ax1.plot(andamento_nazione.index, andamento_nazione['volume_rolling_7d'],
                 color='darkblue', linewidth=3, label='Trend (Media Mobile 7gg)')

        texts_vol = []
        for data_picco, riga in picchi_nazione.iterrows():
            volume_picco = riga['volume']
            ax1.plot(data_picco, volume_picco, 'ro', markersize=10,
                     markeredgecolor='red', markeredgewidth=2,
                     markerfacecolor='none',
                     label='Picco Significativo' if data_picco == picchi_nazione.index[0] else "")
            ax1.axvline(x=data_picco, color='red', linestyle='--', alpha=0.3, linewidth=1)
            data_formattata = data_picco.strftime('%d/%m')
            t = ax1.text(data_picco, volume_picco, f'{data_formattata}\n{volume_picco:.0f} commenti',
                         fontsize=9, fontweight='bold', color='red',
                         ha='center', va='bottom',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='red'))
            texts_vol.append(t)

        # Regola automaticamente la posizione delle etichette dei picchi
        adjust_text(texts_vol, ax=ax1, arrowprops=dict(arrowstyle='->', color='red', alpha=0.6))

        ax1.set_title(f'EVOLUZIONE TEMPORALE CON EVENTI - r/{nazione}\nVolume Commenti e Picchi Significativi',
                      fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('Commenti per Giorno', fontweight='bold')
        ax1.legend(loc='upper left')
        ax1.grid(alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # 2️ SENTIMENT
        ax2.plot(andamento_nazione.index, andamento_nazione['sentiment_medio'],
                 color='red', alpha=0.6, linewidth=1, label='Sentiment Giornaliero')
        ax2.plot(andamento_nazione.index, andamento_nazione['sentiment_rolling_7d'],
                 color='darkred', linewidth=2, label='Trend Sentiment')
        ax2.fill_between(andamento_nazione.index,
                         andamento_nazione['sentiment_medio'] - andamento_nazione['sentiment_std'],
                         andamento_nazione['sentiment_medio'] + andamento_nazione['sentiment_std'],
                         alpha=0.1, color='red')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=1)

        picchi_sentiment = andamento_nazione[
            (andamento_nazione['sentiment_medio'] > andamento_nazione['sentiment_medio'].mean() + andamento_nazione['sentiment_std']) |
            (andamento_nazione['sentiment_medio'] < andamento_nazione['sentiment_medio'].mean() - andamento_nazione['sentiment_std'])
        ]

        texts_sent = []
        for data_picco, riga in picchi_sentiment.head(15).iterrows():
            sentiment_picco = riga['sentiment_medio']
            ax2.plot(data_picco, sentiment_picco, 'ro', markersize=8, alpha=0.8)
            data_formattata = data_picco.strftime('%d/%m')
            t = ax2.text(data_picco, sentiment_picco, f'{data_formattata}\n{sentiment_picco:.3f}',
                         fontsize=8, fontweight='bold', color='red',
                         ha='left', va='bottom' if sentiment_picco >= 0 else 'top',
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='red'))
            texts_sent.append(t)

        adjust_text(texts_sent, ax=ax2, arrowprops=dict(arrowstyle='->', color='red', alpha=0.6))

        ax2.set_ylabel('Polarità Sentiment', fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)

        # 4️ LEGENDA EVENTI
        ax3.axis('off')
        stats_text = (f"📊 STATISTICHE r/{nazione}: "
                      f"Commenti Totali: {len(df_nazione):,} | "
                      f"Sentiment Medio: {df_nazione['polarita'].mean():.3f} | "
                      f"Engagement Medio: {df_nazione['comment_score'].mean():.1f}")

        eventi_testo = "PICCHI IDENTIFICATI:\n"
        if picchi_nazione.empty:
            eventi_testo += "Nessun picco significativo identificato\n"
        else:
            for i, (data_picco, riga) in enumerate(picchi_nazione.head(5).iterrows()):
                data_completa = data_picco.strftime('%d/%m/%Y')
                eventi_testo += f"• {data_completa}: {riga['volume']:.0f} commenti (sentiment: {riga['sentiment_medio']:.3f})\n"

        ax3.text(0.02, 0.8, stats_text, transform=ax3.transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        ax3.text(0.02, 0.3, eventi_testo, transform=ax3.transAxes, fontsize=9,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        plt.tight_layout()

        # Salva il grafico
        os.makedirs(cartella_grafici, exist_ok=True)
        filename = f"{cartella_grafici}/eventi_timeline_{nazione}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        nazioni_analizzate += 1
        print(f"    ----> Grafico eventi salvato: {filename}")
        print(f"            - Picchi identificati: {len(picchi_nazione)}")

    print("=" * 80)
    print(" " * 30, "GRAFICI EVENTI COMPLETATI:")
    return nazioni_analizzate

# ------------------------------------------------------------
# REPORT EVENTI GLOBALI (aggregati) + PICCHI PER NAZIONE
# ------------------------------------------------------------


def crea_report_eventi_globali(df_temporale, eventi_significativi=None):
    print("\n" + "-" * 50 + "> CREAZIONE REPORT EVENTI GLOBALI...")

    cartella_grafici = "grafici_eventi_nazioni"
    os.makedirs(cartella_grafici, exist_ok=True)

    # ========================================================
    # 1️ AGGREGAZIONE GLOBALE (tutti i subreddit insieme)
    # ========================================================
    andamento_globale = df_temporale.groupby('data_giorno').agg({
        'comment_id': 'count',
        'polarita': 'mean',
        'comment_score': 'mean'
    }).rename(columns={
        'comment_id': 'volume',
        'polarita': 'sentiment_medio',
        'comment_score': 'engagement_medio'
    })

    # se ci sono temi dominanti (topic) nel dataset li includiamo
    if 'dominant_topics' in df_temporale.columns:
        temi_dominanti = (
            df_temporale.groupby('data_giorno')['dominant_topics']
            .apply(lambda x: ', '.join(pd.Series(x).dropna().astype(str).unique()[:3]))
        )
        andamento_globale = andamento_globale.join(temi_dominanti)

    # ========================================================
    # 2️IDENTIFICAZIONE PICCHI GLOBALI
    # ========================================================
    volume_medio_globale = andamento_globale['volume'].mean()
    volume_std_globale = andamento_globale['volume'].std()
    picchi_globali = andamento_globale[andamento_globale['volume'] > volume_medio_globale + volume_std_globale]

    picchi_globali = picchi_globali.reset_index().sort_values(by='volume', ascending=False)

    # ========================================================
    # 3️ AGGREGAZIONE PER NAZIONE (come prima)
    # ========================================================
    tutti_picchi_nazionali = []
    for nazione in df_temporale['subreddit'].unique():
        df_nazione = df_temporale[df_temporale['subreddit'] == nazione]
        if len(df_nazione) < 10:
            continue

        andamento_nazione = df_nazione.groupby('data_giorno').agg({
            'comment_id': 'count',
            'polarita': 'mean',
            'comment_score': 'mean'
        }).rename(columns={
            'comment_id': 'volume',
            'polarita': 'sentiment_medio',
            'comment_score': 'engagement_medio'
        })

        volume_medio = andamento_nazione['volume'].mean()
        volume_std = andamento_nazione['volume'].std()
        picchi_nazione = andamento_nazione[andamento_nazione['volume'] > volume_medio + volume_std].copy()
        picchi_nazione['subreddit'] = nazione

        tutti_picchi_nazionali.append(picchi_nazione)

    df_picchi_per_nazione = (
        pd.concat(tutti_picchi_nazionali)
        .reset_index()
        .sort_values(by=['subreddit', 'data_giorno'])
        if tutti_picchi_nazionali else pd.DataFrame()
    )

    # ========================================================
    # 4️SALVATAGGIO DEI CSV
    # ========================================================
    percorso_globali = os.path.join(cartella_grafici, "report_picchi_globali.csv")
    picchi_globali.to_csv(percorso_globali, index=False, encoding='utf-8-sig')

    #percorso_per_nazione = os.path.join(cartella_grafici, "report_picchi_per_nazione.csv")
    #df_picchi_per_nazione.to_csv(percorso_per_nazione, index=False, encoding='utf-8-sig')

    print(f"----> CSV globale salvato: {percorso_globali}")
    #print(f"----> CSV per nazioni salvato: {percorso_per_nazione}")
    print("=" * 80)
    print(f"REPORT EVENTI COMPLETATI: {len(picchi_globali)} picchi globali totali salvati.")

    # ========================================================
    # 5️RITORNO DATI (per uso successivo)
    # ========================================================
    return {
        "picchi_globali": picchi_globali,
        "picchi_per_nazione": df_picchi_per_nazione
    }