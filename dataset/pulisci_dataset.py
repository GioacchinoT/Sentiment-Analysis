import pandas as pd
import re

#####################################################################################################################################

# RIMUOVE COMMENTI RACCOLTI CHE NON CONTENGONO NESSUNA KEYWORD

#####################################################################################################################################

# Carica il dataset
df = pd.read_csv("TRADUTTORI/subset_tradotti/commenti_italia_processato_TRADOTTO.csv")  
# Mappatura delle keyword per lingua (prese dal tuo script di raccolta)

commenti_vuoti = 0

keywords_by_country = {
    "france": ["gaza", "Gaza", "Palestine", "palestine", "israel", "Israel", "israël", "Hamas", "hamas"],
    "de": ["gaza", "palästina", "israel", "hamas","Gaza", "Palästina", "Israel", "Hamas"],
    "italy": ["gaza", "palestina", "israele", "hamas","Gaza", "Palestina", "Israele", "Hamas"],
    "italia": ["gaza", "palestina", "israele", "hamas","Gaza", "Palestina", "Israele", "Hamas", "israeliana", "antisemita", "palestinese", "palestinesi", "Netanyahu", "proteste", "israeliani"],
    "unitedkingdom": ["gaza", "palestine", "israel", "hamas","Gaza", "Palestine", "Israel", "Hamas"],
    "spain": ["gaza", "palestina", "israel", "hamas", "Gaza", "Palestina", "Israel", "Hamas"],
    "poland": ["gaza", "palestyna", "izrael", "hamas", "Gaza", "Palestyna", "Izrael", "Hamas"],
    "netherlands": ["gaza", "palestina", "israël", "hamas", "Gaza", "Palestina", "Israël", "Hamas"],  
    "sweden": ["gaza", "Gaza", "palestina", "Palestina", "israel", "Israel", "hamas", "Hamas"], 
    "norway": ["gaza", "Gaza", "palestina", "Palestina", "israel", "Israel", "hamas", "Hamas"],  
    "denmark": ["gaza", "Gaza", "palestina", "Palestina", "israel", "Israel", "hamas", "Hamas"], 
    "ukraine": ["gaza", "Gaza", "Газа", "палестина", "Палестина", "ізраїль", "Ізраїль", "хамас", "Хамас"],  
    "portugal": ["gaza", "Gaza", "palestina", "Palestina", "israel", "Israel", "hamas", "Hamas"], 
    "greece": ["gaza", "Gaza", "γάζα", "Γάζα", "παλαιστίνη", "Παλαιστίνη", "Ισραήλ", "χαμάς", "Χαμάς"],  
    "hungary": ["gaza", "Gaza", "palesztina", "Palesztina", "izrael", "Izrael", "hamász", "Hamász"], 
    "austria": ["gaza", "Gaza", "palästina", "Palästina", "israel", "Israel", "hamas", "Hamas"],  
    "switzerland": ["gaza", "Gaza", "palästina", "Palästina", "israel", "Israel", "hamas", "Hamas"],  
    "ireland": ["gaza", "Gaza", "palestine", "Palestine", "israel", "Israel", "hamas", "Hamas"], 
    "belgium": ["gaza", "Gaza", "palestine", "Palestine", "israel", "Israel", "hamas", "Hamas"],
    "czech": ["gaza", "Gaza", "palestina", "Palestina", "izrael", "Izrael", "hamas", "Hamas"],  
    "romania": ["gaza", "Gaza", "palestina", "Palestina", "israel", "Israel", "hamas", "Hamas"]  
}



def post_has_keyword(post_title, subreddit, comment_text):
    """
    Verifica se il post_title contiene ALMENO UNA keyword per quel subreddit
    """
    if subreddit not in keywords_by_country:
        return False
    
    global commenti_vuoti

    if pd.isna(comment_text):
        comment_text = str(comment_text)
        commenti_vuoti += 1
        if comment_text == "nan":
            return False
    

    title_lower = post_title.lower()
    comment_lower = comment_text.lower()
    keywords = keywords_by_country[subreddit]
    
    # Cerca ALMENO UNA keyword nel titolo OPPURE nel commento
    for keyword in keywords:
        kw = keyword.lower()
        if (kw in title_lower) or (kw in comment_lower):
            return True

    return False

# STATISTICHE PRIMA DELLA PULIZIA
print("STATISTICHE PRIMA DELLA PULIZIA:")
print(f"Totale commenti: {len(df):,}")
print(f"Post unici: {df['post_id'].nunique()}")
print(f"Subreddit: {df['subreddit'].nunique()}")

# Identifica i post che hanno keyword nel titolo
print("\n Analizzando i post...")
righe_da_salvare = []
righe_da_rimuovere = []

for index, row in df.iterrows():
    has_keyword = post_has_keyword(row['post_title'], row['subreddit'], row['comment_text'])
    if has_keyword:
        righe_da_salvare.append(row)
    else:
        righe_da_rimuovere.append(row)

df_pulito = pd.DataFrame(righe_da_salvare)
df_rimossi = pd.DataFrame(righe_da_rimuovere)

df_pulito.to_csv('dataset/NULLO.csv', index=False)
df_rimossi.to_csv('commenti_RIMOSSI.csv', index=False)

# STATISTICHE DOPO LA PULIZIA
print(f"STATISTICHE DOPO LA PULIZIA:")
print(f"Totale commenti: {len(df_pulito):,}")
print(f"Post unici rimasti: {df_pulito['post_id'].nunique()}")
print(f"Commenti rimossi: {len(df_rimossi):,}")

# Analisi per subreddit dei dati RIMOSSI
print(f"\n ANALISI DATI RIMOSSI:")
removed_stats = df_rimossi.groupby('subreddit').agg({
    'post_id': 'nunique',
    'comment_id': 'count'
}).rename(columns={'post_id': 'post_rimossi', 'comment_id': 'commenti_rimossi'})

print(removed_stats)
print(f"Efficienza pulizia: {(len(df_pulito)/len(df)*100):.1f}% dei commenti mantenuti")
print(f"Rumore eliminato: {(len(df_rimossi)/len(df)*100):.1f}% dei commenti rimossi")

print(commenti_vuoti, "<-- commenti vuoti")
