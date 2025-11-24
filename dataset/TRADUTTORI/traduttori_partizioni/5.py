# traduttore_singola_partizione_CORRETTO.py
import pandas as pd
from deep_translator import GoogleTranslator
import time
import sys
import os
from tqdm import tqdm

def verifica_colonne(df):
    """
    Verifica e sistema i nomi delle colonne
    """
    print("--> Verifica colonne disponibili...")
    print(f"   Colonne trovate: {list(df.columns)}")
    
    # Rinomina comment_body in comment_text se esiste
    if 'comment_body' in df.columns and 'comment_text' not in df.columns:
        df = df.rename(columns={'comment_body': 'comment_text'})
        print("   --> Rinomina: comment_body -> comment_text")
    
    # Verifica 
    colonne_necessarie = ['subreddit', 'comment_text', 'post_title']
    colonne_trovate = [col for col in colonne_necessarie if col in df.columns]
    colonne_mancanti = [col for col in colonne_necessarie if col not in df.columns]
    
    if colonne_mancanti:
        print(f"   -> Colonne mancanti: {colonne_mancanti}")
        return None
    else:
        print(f"   -> Colonne essenziali trovate: {colonne_trovate}")
        return df

def setup_mappatura_lingue():
    """
    Mappatura subreddit -> lingua
    """
    return{
    'france': 'fr',
    'de': 'de', 
    'italy': 'it',
    'unitedkingdom': 'en',
    'spain': 'es',
    'poland': 'pl',
    'netherlands': 'nl',
    'sweden': 'sv',
    'norway': 'no',
    'denmark': 'da',
    'ukraine': 'uk',
    'portugal': 'pt',
    'greece': 'el',
    'hungary': 'hu',
    'austria': 'de',
    'switzerland': 'de',
    'ireland': 'ga',
    'belgium': 'nl',
    'czech': 'cs',
    'romania': 'ro'
}

def traduci_testo(testo, lingua_originale,):
    """
    Traduci testo con gestione errori robusta
    """
    if lingua_originale == 'en':
        return testo  # --> già in inglese
    
    if not isinstance(testo, str) or len(testo.strip()) < 2:
        return testo
    
    # lunghezza limitata per evitare errori API
    testo_da_tradurre = str(testo)[:3000]
    
    tentativo = 0
    max_retries = 20

    while(tentativo < max_retries):

    #for tentativo in range(max_retries):
        try:
            tradotto = GoogleTranslator(
                source=lingua_originale, 
                target='en'
            ).translate(text=testo_da_tradurre)
            
            # Rate limiting
            time.sleep(0.3)
            return tradotto
            
        except Exception as e:
            error_type = str(e)
            if "Connection" in error_type or "Remote" in error_type:
                print("X" *20, f" Errore connessione, tentativo {tentativo + 1}/{max_retries}")
                time.sleep(5)
            elif "too many requests" in error_type.lower():
                print(f"     Rate limit, pausa più lunga...")
                time.sleep(10)
            else:
                print(f"    Errore traduzione: {error_type[:100]}")
                break
    
    # Fallback: ritorna testo originale
    return testo

def traduci_partizione(file_path_partizione):
    """
    Traduce una singola partizione del dataset
    """
    print(f"--------> TRADUZIONE PARTIZIONE: {file_path_partizione}")
    
    # Carica la partizione
    try:
        df = pd.read_csv(file_path_partizione, engine='python', on_bad_lines='skip')
        print(f"   -> Partizione caricata: {len(df)} righe")
    except Exception as e:
        print(f"   -> Errore caricamento: {e}")
        return None
    
    # Verifica e sistema colonne
    df = verifica_colonne(df)
    if df is None:
        print("   -> Colonne essenziali mancanti!")
        return None
    
    # Mappatura lingue
    mappatura_lingue = setup_mappatura_lingue()
    df['lingua_originale'] = df['subreddit'].map(mappatura_lingue).fillna('en')
    
    # Statistiche lingue
    lingue_stats = df['lingua_originale'].value_counts()
    print(f"-> DISTRIBUZIONE LINGUE:")
    for lingua, conteggio in lingue_stats.items():
        percentuale = (conteggio / len(df)) * 100
        print(f"   -> {lingua}: {conteggio} commenti ({percentuale:.1f}%)")
    

    commenti_tradotti = []
    titoli_tradotti = []
    
    errori_traduzione = 0
    
    #PROGRESS BAR
    print("--->  INIZIO TRADUZIONE...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Traduzione"):
        lingua = row['lingua_originale']
        
        try:
            # TRADUCI COMMENTO 
            if lingua == 'en':
                commento_tradotto = row['comment_text']
            else:
                commento_tradotto = traduci_testo(row['comment_text'], lingua)
                if commento_tradotto == row['comment_text']:
                    errori_traduzione += 1
            
            commenti_tradotti.append(commento_tradotto)
            
            # TRADUCI TITOLO
            if lingua == 'en':
                titolo_tradotto = row['post_title']
            else:
                titolo_tradotto = traduci_testo(row['post_title'], lingua)
            
            titoli_tradotti.append(titolo_tradotto)
                
        except Exception as e:
            # Fallback in caso di errore generico
            commenti_tradotti.append(row['comment_text'])
            titoli_tradotti.append(row['post_title'])
            errori_traduzione += 1
    
    # Aggiorna dataframe con testi tradotti
    df['comment_text'] = commenti_tradotti
    df['post_title'] = titoli_tradotti
    
    nome_file = os.path.basename(file_path_partizione).replace('.csv', '_TRADOTTO.csv')
    file_output = os.path.join("TRADUTTORI/subset_tradotti", nome_file)      
    try:
        df.to_csv(file_output, index=False, encoding='utf-8-sig')
        print(f"-> COMPLETATO: {file_output}")
        print(f"   > Righe tradotte: {len(df)}")
        print(f"   > Errori traduzione: {errori_traduzione}")
        print(f"   > File di output: {file_output}")
        
        return file_output
        
    except Exception as e:
        print(f"-> Errore salvataggio: {e}")
        return None



if __name__ == "__main__":
    
    partizione_path = "TRADUTTORI/subset/partizione_05_di_10.csv"
    
    if not os.path.exists(partizione_path):
        print(f"-> File non trovato: {partizione_path}")
        sys.exit(1)
    
    risultato = traduci_partizione(partizione_path)
    
    if risultato:
        print(f"-> PARTIZIONE TRADOTTA CON SUCCESSO!")
    else:
        print(f"-> ERRORE NELLA TRADUZIONE")
        sys.exit(1)