# modulo2_5_post_virali.py

import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

def analizza_post_piu_commentati(df, top_n=10):
    """
    Analizza i post che hanno generato più discussioni per ogni nazione
    """
    print("\n ANALISI POST PIÙ COMMENTATI PER NAZIONE")
    print("=" * 60)
    
    # Crea cartella per i risultati
    cartella_risultati = "analisi_post_virali"
    if not os.path.exists(cartella_risultati):
        os.makedirs(cartella_risultati)
    
    risultati_per_nazione = {}
    
    for nazione in df['subreddit'].unique():
        df_nazione = df[df['subreddit'] == nazione]
    
        
        # Estrai la data del post (primo comment_created per ogni post)
        date_post = df_nazione.groupby(['post_id', 'post_title'])['comment_created'].min()
        
        # Raggruppa per post e calcola metriche
        post_metrics = df_nazione.groupby(['post_id', 'post_title']).agg({
            'comment_id': 'count',
            'comment_score': ['sum', 'mean', 'max'],
            'comment_created': ['min', 'max']  # Primo e ultimo commento
        }).round(3)
        
        # Appiattisci le colonne multi-indice
        post_metrics.columns = [
            'numero_commenti', 'upvotes_totali', 'upvote_medio', 'upvote_max',
            'primo_commento', 'ultimo_commento'
        ]
        
        # Aggiungi la data del post
        post_metrics['data_post'] = date_post
        
        # Aggiungi colonne sentiment solo se esistono
        if 'polarita' in df_nazione.columns:
            sentiment_metrics = df_nazione.groupby(['post_id', 'post_title']).agg({
                'polarita': 'mean',
                'soggettivita': 'mean'
            }).round(3)
            post_metrics['sentiment_medio'] = sentiment_metrics['polarita']
            post_metrics['soggettivita_media'] = sentiment_metrics['soggettivita']
        else:
            post_metrics['sentiment_medio'] = 0
            post_metrics['soggettivita_media'] = 0
        
        # Calcola durata discussione in giorni
        post_metrics['durata_discussione_giorni'] = (
            post_metrics['ultimo_commento'] - post_metrics['primo_commento']
        ).dt.total_seconds() / (24 * 3600)
        
        # Calcola engagement rate
        post_metrics['engagement_rate'] = (
            post_metrics['upvotes_totali'] / post_metrics['numero_commenti']
        ).round(2)
        
        # Ordina per numero di commenti (più discussi)
        post_piu_commentati = post_metrics.nlargest(top_n, 'numero_commenti')
        
        # Aggiungi al risultato
        risultati_per_nazione[nazione] = {
            'tutti_i_post': post_metrics,
            'top_post': post_piu_commentati,
            'statistiche': {
                'post_totali': len(post_metrics),
                'commenti_totali': len(df_nazione),
                'commenti_per_post_medio': len(df_nazione) / len(post_metrics),
                'post_piu_commentato': post_piu_commentati.iloc[0] if not post_piu_commentati.empty else None
            }
        }
    
    return risultati_per_nazione

def crea_report_post_virali(risultati_per_nazione):

    print("\n")
    print("-"*20, "> CREAZIONE REPORT POST VIRALI...")
    
    cartella_risultati = "analisi_post_virali"
    
    # 1. REPORT TESTO PER OGNI NAZIONE
    for nazione, risultati in risultati_per_nazione.items():
        filename = f"{cartella_risultati}/top_post_{nazione}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f" REPORT POST PIÙ COMMENTATI - r/{nazione}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"STATISTICHE GENERALI:\n")
            f.write(f"> Post totali analizzati: {risultati['statistiche']['post_totali']}\n")
            f.write(f"> Commenti totali: {risultati['statistiche']['commenti_totali']:,}\n")
            f.write(f"> Commenti per post (media): {risultati['statistiche']['commenti_per_post_medio']:.1f}\n\n")
            
            f.write("TOP 10 POST PIÙ COMMENTATI:\n")
            f.write("-" * 80 + "\n")
            
            for i, (post_id, stats) in enumerate(risultati['top_post'].iterrows()):
                # Formatta le date
                data_post = stats['data_post'].strftime('%d/%m/%Y')
                data_primo_commento = stats['primo_commento'].strftime('%d/%m/%Y %H:%M')
                data_ultimo_commento = stats['ultimo_commento'].strftime('%d/%m/%Y %H:%M')
                
                f.write(f"\n#{i+1} - {stats['numero_commenti']} COMMENTI\n")
                f.write(f"-Data post: {data_post}\n")
                f.write(f"-Titolo: {stats.name[1]}\n")
                f.write(f"-Post ID: {post_id}\n")
                f.write(f"-Metriche:\n")
                f.write(f"  > Commenti: {stats['numero_commenti']}\n")
                f.write(f"  > Upvotes totali: {stats['upvotes_totali']:,}\n")
                f.write(f"  > Upvote medio: {stats['upvote_medio']:.1f}\n")
                f.write(f"  > Upvote massimo: {stats['upvote_max']}\n")
                f.write(f"  > Sentiment medio: {stats['sentiment_medio']:.3f}\n")
                f.write(f"  > Soggettività: {stats['soggettivita_media']:.3f}\n")
                f.write(f"  > Engagement rate: {stats['engagement_rate']:.2f}\n")
                f.write(f"  > Durata discussione: {stats['durata_discussione_giorni']:.1f} giorni\n")
                f.write(f"  > Primo commento: {data_primo_commento}\n")
                f.write(f"  > Ultimo commento: {data_ultimo_commento}\n")
                f.write("-" * 40 + "\n")
        
        print(f"    ..Report salvato: {filename}")
    
    # 3. GRAFICO COMPARATIVO TRA NAZIONI
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))
    
    # Prepara dati per grafici comparativi
    nazioni = []
    commenti_medi = []
    engagement_medi = []
    sentiment_medi = []
    post_top_commenti = []
    
    for nazione, risultati in risultati_per_nazione.items():
        if not risultati['top_post'].empty:
            nazioni.append(nazione)
            commenti_medi.append(risultati['statistiche']['commenti_per_post_medio'])
            engagement_medi.append(risultati['top_post']['engagement_rate'].mean())
            sentiment_medi.append(risultati['top_post']['sentiment_medio'].mean())
            post_top_commenti.append(risultati['top_post'].iloc[0]['numero_commenti'])
    
    # Grafico 1: Commenti medi per post
    if nazioni:
        bars1 = ax1.bar(nazioni, commenti_medi, color='skyblue', alpha=0.7)
        ax1.set_title('Commenti Medi per Post per Nazione', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Commenti per Post')
        ax1.tick_params(axis='x', rotation=45)
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Grafico 2: Engagement rate medio
        bars2 = ax2.bar(nazioni, engagement_medi, color='lightgreen', alpha=0.7)
        ax2.set_title('Engagement Rate Medio (Upvotes/Commento)', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Engagement Rate')
        ax2.tick_params(axis='x', rotation=45)
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Grafico 3: Sentiment medio post top
        bars3 = ax3.bar(nazioni, sentiment_medi, color='lightcoral', alpha=0.7)
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax3.set_title('Sentiment Medio dei Post Più Commentati', fontweight='bold', fontsize=12)
        ax3.set_ylabel('Polarità Sentiment')
        ax3.tick_params(axis='x', rotation=45)
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Grafico 4: Post con più commenti per nazione
        bars4 = ax4.bar(nazioni, post_top_commenti, color='gold', alpha=0.7)
        ax4.set_title('Post Singolo con Più Commenti per Nazione', fontweight='bold', fontsize=12)
        ax4.set_ylabel('Numero Commenti')
        ax4.tick_params(axis='x', rotation=45)
        for bar in bars4:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{height:.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{cartella_risultati}/comparazione_post_virali.png', dpi=300, bbox_inches='tight')
        print(f"-----> Grafico comparativo salvato: {cartella_risultati}/comparazione_post_virali.png")
    else:
        print(" -----> Nessun dato sufficiente per creare grafici comparativi")
    
    return risultati_per_nazione

def genera_analisi_post_virali(df):

    print("\n")
    print("="*50, "> AVVIO ANALISI POST VIRALI (modulo post_più_commentati)")
    
    # Analizza i post più commentati
    risultati = analizza_post_piu_commentati(df, top_n=15)
    
    # Crea report e visualizzazioni
    risultati_completi = crea_report_post_virali(risultati)
    
    print(f"\n ANALISI POST VIRALI COMPLETATA! -----------> File salvati in: analisi_post_virali/")
    
    return risultati_completi
