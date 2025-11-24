
def sistema_categorizzazione():

    #categorizzazione commenti per tema

    temi = {
        'international_politics': {
            'keywords': ['government', 'united nations', 'eu', 'nato', 'sanctions', 'diplomacy', 'international', 'policy', 'foreign', 'relations', 'summit', 'negotiation', 'treaty', 'alliance', 'security'],
            'description': 'International politics and relations'
        },
        
        'media_narrative': {
            'keywords': ['media', 'news', 'coverage', 'propaganda', 'narrative', 'biased', 'journalism', 'reporting', 'press', 'article', 'story', 'information', 'truth', 'fake', 'manipulation'],
            'description': 'Media discussions and narrative'
        },
        
        'violence_protests': {
            'keywords': ['violence', 'clash', 'riot', 'protest', 'demonstration', 'police', 'security', 'confrontation', 'attack', 'force', 'unrest', 'turmoil', 'conflict', 'struggle', 'resistance'],
            'description': 'Violence during protests'
        },
        
        'solidarity_support': {
            'keywords': ['solidarity', 'support', 'peace', 'ceasefire', 'truce', 'dialogue', 'humanity', 'compassion', 'help', 'aid', 'unity', 'cooperation', 'understanding', 'empathy', 'hope'],
            'description': 'Expressions of solidarity and peace appeals'
        },
        
        'human_rights': {
            'keywords': ['human rights', 'civilians', 'victims', 'humanitarian', 'crisis', 'children', 'population', 'civilian', 'casualties', 'suffering', 'innocent', 'protection', 'dignity', 'freedom', 'justice'],
            'description': 'Humanitarian issues and fundamental rights'
        },
        
        'economic_consequences': {
            'keywords': ['economy', 'economic', 'sanctions', 'trade', 'market', 'financial', 'cost', 'price', 'inflation', 'recession', 'crisis', 'investment', 'business', 'industry', 'development'],
            'description': 'Economic consequences of the conflict'
        },
        
        'government_criticism': {
            'keywords': ['government', 'leader', 'policy', 'decision', 'failure', 'mistake', 'wrong', 'incompetent', 'corrupt', 'responsible', 'accountable', 'blame', 'criticism', 'protest', 'opposition'],
            'description': 'Criticism of governments and leadership'
        }
    }
    
    return temi

def categorizza_commento(testo, temi):


    if not isinstance(testo, str) or len(testo) < 10: #lunghezza impostata a > di 10 in quanto commenti corti non contengono discussioni
        return []
    
    testo_lower = testo.lower()
    testo_pulito = ' ' + testo_lower + ' '
    temi_rilevanti = []
    
    for tema, info in temi.items():
        punteggio_tema = 0
        
        for keyword in info['keywords']:
            # Match esatto con spazi
            if f' {keyword} ' in testo_pulito:
                punteggio_tema += 3.0
                break  # Un match esatto è sufficiente
        
        if punteggio_tema == 0:
            # Match parziale
            for keyword in info['keywords']:
                if keyword in testo_lower:
                    punteggio_tema += 2.0
                    break
        
        if punteggio_tema == 0:
            # Match radice per parole lunghe
            parole_testo = testo_lower.split()
            for keyword in info['keywords']:
                if len(keyword) > 3:
                    radice = keyword[:4]
                    if any(parola.startswith(radice) for parola in parole_testo):
                        punteggio_tema += 1.5
                        break
        
        # Soglia messa a 1 match
        if punteggio_tema >= 1.0:
            temi_rilevanti.append(tema)
    
    return list(set(temi_rilevanti))

def applica_categorizzazione(df):
    
    print("\n")
    print("="*50, "> APPLICAZIONE CATEGORIZZAZIONE TEMATICA ... (modulo 3_1) ")
    
    # Carica sistema di categorizzazione
    temi_commenti = sistema_categorizzazione()
    
    # Applica categorizzazione
    df['temi_rilevanti'] = df['comment_text'].apply(
        lambda x: categorizza_commento(x, temi_commenti)
    )
    
    # Statistiche
    commenti_categorizzati = df[df['temi_rilevanti'].apply(len) > 0].shape[0]
    percentuale_categorizzati = (commenti_categorizzati / len(df)) * 100
    
    print(f"\n--> RISULTATI CATEGORIZZAZIONE:")
    print(f"   > Commenti categorizzati: {commenti_categorizzati:,}/{len(df):,} ({percentuale_categorizzati:.1f}%)")
    print(f"   > Temi per commento (media): {df['temi_rilevanti'].apply(len).mean():.2f}")
    
    # Prepara colonne binarie per ogni tema
    df['numero_temi'] = df['temi_rilevanti'].apply(len)
    
    for tema in temi_commenti.keys():
        df[f'tema_{tema}'] = df['temi_rilevanti'].apply(lambda x: 1 if tema in x else 0)
    
   
    # Analisi cross-nazionale
    print(f"\n--> COMMENTI CATEGORIZZATI PER NAZIONE:")
    for nazione in df['subreddit'].unique()[:10]:  # Prime 10 nazioni
        df_nazione = df[df['subreddit'] == nazione]
        if len(df_nazione) > 0:
            percentuale_categorizzati_nazione = (df_nazione['numero_temi'] > 0).sum() / len(df_nazione) * 100
            print(f"   > r/{nazione}: {len(df_nazione):,} commenti, {percentuale_categorizzati_nazione:.1f}% categorizzati")
    
    return df, temi_commenti


