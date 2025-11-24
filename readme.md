# Sentiment Analysis dell'Opinione Pubblica sul Conflitto a Gaza: Studio Comparativo su Reddit in Ambito Europeo
## 📖 Descrizione del Progetto

Questo progetto universitario propone un'analisi computazionale estensiva delle dinamiche di opinione, del sentiment e dell'evoluzione tematica riguardanti il conflitto di Gaza all'interno di 20 comunità nazionali europee sulla piattaforma Reddit.

Attraverso tecniche di **Natural Language Processing (NLP)**, analisi delle serie storiche e clustering non supervisionato, lo studio ha esaminato oltre **141.000 commenti** raccolti in un arco temporale di 369 giorni (Ottobre 2024 - Ottobre 2025), con l'obiettivo di comprendere come shock globali ed eventi locali influenzino il dibattito pubblico digitale in Europa.

### Obiettivi Principali
1.  **Mappatura Comparativa:** Classificare le nazioni in base a volume di attività e qualità dell'engagement.
2.  **Analisi Tematica:** Identificare i temi dominanti (es. *International Politics*, *Solidarity*, *Violence*) e la loro distribuzione geografica.
3.  **Sentiment Analysis:** Misurare la polarità emotiva e la soggettività delle discussioni.
4.  **Studio Temporale:** Distinguere tra eventi **sincroni** (shock globali) e **asincroni** (tensioni domestiche).

---

## Architettura e Pipeline

Il progetto è strutturato in un'architettura modulare sequenziale in Python, divisa in 5 fasi logiche:

* **Fase 1: Data Collection & Preprocessing**
    * Pulizia del dataset, gestione missing values, filtraggio per lunghezza (>5 char) e standardizzazione temporale.
* **Fase 2: Analisi Comparativa (Clustering)**
    * Utilizzo di *K-Means* per segmentare le nazioni in 4 cluster comportamentali (es. "Alta Intensità/Basso Engagement" vs "Alta Qualità/Basso Volume").
* **Fase 3: Analisi Tematica (Rule-Based)**
    * Classificazione dei commenti in 7 macro-temi tramite dizionari di keyword pesate.
* **Fase 4: Sentiment Analysis**
    * Calcolo di *Polarity* e *Subjectivity* tramite `TextBlob`.
    * Analisi della correlazione tra temi e sentiment.
* **Fase 5: Analisi Temporale e Trend**
    * Costruzione di serie temporali giornaliere.
    * Rilevamento statistico dei picchi di volume ($\mu + \sigma$) e studio degli eventi *trigger*.

---

## Struttura del Repository


```bash
├── FASI/                           # Cartella principale del codice sorgente
│   ├── FASE2/                      # Moduli per Analisi Comparativa
│   ├── FASE3/                      # Moduli per Analisi Tematica
│   ├── FASE4/                      # Moduli per Sentiment Analysis
│   ├── FASE5/                      # Moduli per Analisi Temporale
│   ├── FILE_GRAFICI_FINALI/        # Script per visualizzazioni finali
│   │   ├── grafici_eventi.py       # Generazione timeline eventi
│   │   └── post_più_commentati.py  # Analisi viralità e top post
│   └── main.py                     # ENTRY POINT: Avvia l'intera analisi
│
├── analisi_post_virali/            # Output: Report sui post più commentati
├── dataset/                        # Input: Contiene il dataset (es. ds_fine.csv)
├── grafici_eventi_nazioni/         # Output: Timeline temporali e picchi
├── report e grafici generati/      # Output: Grafici generali (bar chart, pie chart, ecc.)
├── risultati/                      # Output: Log testuali dell'esecuzione (file .txt)
└── TEMATICHE PER TEMPO/            # Output: Grafici evoluzione temi
```

Istruzioni per l'Esecuzione
Il sistema è progettato per essere eseguito interamente tramite un unico entry point che sequenzia automaticamente tutte le fasi dell'analisi.

1. Avvio dell'Analisi
Per eseguire il programma completo, posizionarsi nella root del progetto ed eseguire il file main.py:

```bash
python main.py
```
2. Output e Risultati
Al termine dell'esecuzione, non è necessario monitorare la console. Tutti i risultati (statistiche, tabelle, log di avanzamento e insight) vengono reindirizzati e salvati automaticamente in un file di testo all'interno della cartella risultati/.

File di output: Il nome del file includerà il timestamp dell'esecuzione (es. risultati/risultati_20251124_103000.txt).

Grafici: Tutte le visualizzazioni generate verranno salvate nelle rispettive cartelle di output (grafici_eventi_nazioni, report e grafici generati, ecc.).