import pandas as pd

############################################################################################################################################

# CONTROLLA CHE DOPO LA PULIZIA DEL DATASET NON SIANO STATE RIMOSSI COMMENTI CONTENENTI KEYWRD, CONTROLLANDO IL DATASET DEI COMMENTI RIMOSSI

#############################################################################################################################################

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

def cerca_commenti():

    df = pd.read_csv("commenti_RIMOSSI.csv")

    for index, row in df.iterrows():

        commento = row['comment_body']
        
        keywords = keywords_by_country[row['subreddit']]
        #print(keywords)
        #if row['subreddit'] == 'italy':
            
            
        #print(row['subreddit'], " --- ", " sono qui")
        for kw in keywords:
            if type(commento) != float:
                if kw in commento or kw in row['post_title']:
                    print("TITOLO POST ------>", row['post_title'])
                    print("keyword ----->", kw)
                    print("\n", commento, "\n")
                    print("-" *40)


cerca_commenti()

