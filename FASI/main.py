import sys
from datetime import datetime
import pandas as pd
from FASE2 import modulo2_1, modulo2_2, modulo2_3, modulo2_4
from FASE3 import modulo3_1, modulo3_2, modulo3_3
from FASE4 import modulo4_1, modulo4_2, modulo4_3,modulo4_4, modulo4_5, modulo4_6
from FASE5 import modulo5_1, modulo5_2, modulo5_3, modulo5_4, modulo5_5
from FILE_GRAFICI_FINALI import post_più_commentati, grafici_eventi


if __name__ == "__main__":
    # Configura pandas per mostrare TUTTE le colonne e righe
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.expand_frame_repr', False)

    # Reindirizza tutto l'output su file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"risultati/risultati_{timestamp}.txt"
    
    # Apri il file con encoding utf-8
    with open(output_file, 'w', encoding='utf-8') as f:
        sys.stdout = f
        
        print(f"Output reindirizzato su: {output_file}")
        print("=" * 60)
        
        try:
            df = modulo2_1.carica_dataset()
            s = modulo2_1.setting_preliminare(df)
            
            if s is not None:
                print("colonne mancanti --> ", s)
            
            #FASE2
            print("\n" + "="*60)
            print(" "*8, "INIZIO ANALISI FASE 2: ANALISI COMPARATIVA NAZIONI")
            print("="*60)

            df = modulo2_1.preprocessing_dati(df)
            metriche_nazioni = modulo2_1.analisi_comparativa(df)
            fig = modulo2_2.crea_visualizzazioni_comparative(metriche_nazioni, df)
            cluster_metriche_nazioni = modulo2_3.analisi_cluster_nazioni(metriche_nazioni)
            modulo2_4.genera_report_fase2(metriche_nazioni, df)

            #FASE 3 

            df_tematico, temi_commenti = modulo3_1.applica_categorizzazione(df)
            df_profilo_tematico, distribuzione_globale = modulo3_2.analisi_tematiche_transnazionali(df_tematico, temi_commenti)
            figura_tematiche = modulo3_3.crea_visualizzazioni_tematiche(df_profilo_tematico, distribuzione_globale, df_tematico)
            
            #FASE 4
            
            df_sentiment = modulo4_1.applica_sentiment(df)
            sentiment_per_nazione, df_sentiment_temi, polarizzazione_per_nazione = modulo4_2.analisi_sentiment_comparata(df_sentiment)
            figura_sentiment = modulo4_3.crea_visualizzazioni_sentiment(sentiment_per_nazione, df_sentiment_temi, polarizzazione_per_nazione, df_sentiment)
            sentiment_per_nazione_cluster = modulo4_4.analisi_cluster_sentiment(df_sentiment, sentiment_per_nazione)
            sentiment_per_tema, combinazioni_significative, matrice_correlazione = modulo4_5.analisi_correlazioni_tematiche_sentiment(df_sentiment)
            sentiment_per_area = modulo4_6.genera_report_fase4(df_sentiment, sentiment_per_nazione, df_sentiment_temi, polarizzazione_per_nazione)

            #NUOVO
            risultati_post_sentiment = modulo4_6.analisi_sentiment_per_post(df_sentiment)

            #FASE 5
            df_temporale = modulo5_1.setup_analisi_temporale(df_sentiment)
            andamento_giornaliero, evoluzione_nazionale, eventi_significativi, pattern_giornaliero, pattern_settimanale = modulo5_2.analisi_evoluzione_temporale(df_temporale)
            figura_temporale = modulo5_3.crea_visualizzazioni_temporali_avanzate(andamento_giornaliero, evoluzione_nazionale, eventi_significativi, pattern_giornaliero, pattern_settimanale, df_temporale)
            risultati_predittivi = modulo5_4.analisi_trend_predittiva(andamento_giornaliero, evoluzione_nazionale)
            modulo5_5.genera_report_fase5_e_conclusione(df_temporale, andamento_giornaliero, evoluzione_nazionale, eventi_significativi, risultati_predittivi)

            nazioni_temi_analizzate = modulo5_3.crea_grafici_temi_temporali_per_nazione(df_temporale)

            ########EVENTI

            nazioni_analizzate = grafici_eventi.crea_grafici_temporali_con_eventi(df_temporale, andamento_giornaliero, evoluzione_nazionale, eventi_significativi)
            grafici_eventi.crea_report_eventi_globali(df_temporale)
            risultati_post_virali = post_più_commentati.genera_analisi_post_virali(df_sentiment)

            

        except Exception as e:
            print(f"ERRORE: {e}")
            import traceback
            traceback.print_exc()

        sys.stdout.close()
        sys.stdout = sys.__stdout__