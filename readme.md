# Sentiment Analysis dell'Opinione Pubblica sul Conflitto a Gaza: Studio Comparativo su Reddit in Ambito Europeo

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Libraries](https://img.shields.io/badge/Library-Pandas%20|%20TextBlob%20|%20Scikit--Learn-orange)
![Status](https://img.shields.io/badge/Status-Completed-green)

## 📖 Descrizione del Progetto

Questo progetto universitario propone un'analisi computazionale estensiva delle dinamiche di opinione, del sentiment e dell'evoluzione tematica riguardanti il conflitto di Gaza all'interno di **20 comunità nazionali europee** sulla piattaforma Reddit.

Attraverso tecniche di **Natural Language Processing (NLP)**, analisi delle serie storiche e clustering non supervisionato, lo studio ha esaminato oltre **141.000 commenti** raccolti in un arco temporale di 369 giorni (Ottobre 2024 - Ottobre 2025), con l'obiettivo di comprendere come shock globali ed eventi locali influenzino il dibattito pubblico digitale in Europa.

### 🎯 Obiettivi Principali
1.  **Mappatura Comparativa:** Classificare le nazioni in base a volume di attività e qualità dell'engagement.
2.  **Analisi Tematica:** Identificare i temi dominanti (es. *International Politics*, *Solidarity*, *Violence*) e la loro distribuzione geografica.
3.  **Sentiment Analysis:** Misurare la polarità emotiva e la soggettività delle discussioni.
4.  **Studio Temporale:** Distinguere tra eventi **sincroni** (shock globali) e **asincroni** (tensioni domestiche).

---

## 🛠️ Architettura e Pipeline

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

## 📊 Risultati Chiave

### 1. Sincronia vs. Asincronia
Lo studio ha rivelato una dicotomia fondamentale nella reattività delle nazioni:
* **Sincronia (Shock Globale):** Eventi come l'escalation militare del **13 Giugno 2025** hanno attivato simultaneamente tutte le nazioni analizzate, abbattendo le barriere linguistiche.
* **Asincronia (Filtro Locale):** I picchi unici per nazione (es. Italia il 16 Settembre) sono innescati da eventi domestici (proteste, politica interna), dove il conflitto diventa uno specchio per le tensioni locali.

### 2. Il Caso Italia (r/italy)
L'Italia emerge come un *outlier* culturale:
* **Alta Polarizzazione:** Registra il picco di negatività assoluta (-1.00) e un'alta polarizzazione, dovuta a un linguaggio più espressivo e binario.
* **Focus Interno:** I picchi di discussione sono spesso legati a problemi di ordine pubblico (*Violence & Protests*) piuttosto che a pura geopolitica.

### 3. Cluster Nazionali
* **Alta Reattività:** Francia, Italia, Irlanda (Alto Volume, Engagement Medio-Basso).
* **Alta Qualità:** Germania, Regno Unito (Volume Minore, Engagement Altissimo, discussioni più analitiche).

---

## 📂 Struttura del Repository

```bash
├── dataset/
│   └── ds_fine.csv          # Dataset processato (non incluso per privacy/dimensioni)
├── analisi_post_virali/     # Report sui post più commentati per nazione
├── grafici_eventi_nazioni/  # Visualizzazioni delle timeline e picchi
├── report e grafici/        # Output grafici generali (Sentiment, Temi)
├── risultati/               # Log testuali delle esecuzioni
├── main.py                  # Orchestratore principale
├── FASE2.py                 # Modulo Analisi Comparativa
├── FASE3.py                 # Modulo Analisi Tematica
├── FASE4.py                 # Modulo Sentiment Analysis
├── FASE5.py                 # Modulo Analisi Temporale
├── grafici_eventi.py        # Utility per generazione grafici temporali
├── post_più_commentati.py   # Utility per analisi viralità
├── utils.py                 # Funzioni di supporto comuni
└── README.md                # Questo file