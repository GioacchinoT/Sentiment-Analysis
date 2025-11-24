
import pandas as pd

########################################################################################################################################

# RIMUOVE COMMENTI RACCOLTI PIU DI UNA VOLTA

########################################################################################################################################
def rimuovi_duplicati_dataset(file_input, file_output):
    """
    Rimuove i duplicati dal dataset basandosi su comment_id
    """
    print(f"Pulizia duplicati: {file_input}")
    colonna_id='comment_id'
    # Carica dataset
    df = pd.read_csv(file_input, engine='python', on_bad_lines='skip')
    print(f"   > Righe prima: {len(df):,}")
    
    # Conta duplicati
    duplicati = df.duplicated(subset=[colonna_id]).sum()
    print(f"   > Duplicati trovati: {duplicati:,}")
    
    # Rimuovi duplicati
    df_pulito = df.drop_duplicates(subset=[colonna_id], keep='first')
    print(f"   > Righe dopo: {len(df_pulito):,}")
    print(f"   > Duplicati rimossi: {duplicati}")
    
    # Salva dataset pulito
    df_pulito.to_csv(file_output, index=False, encoding='utf-8')
    print(f"----> Dataset pulito salvato: {file_output}")
    
    return df_pulito


def verifica_duplicati(file_originale, file_pulito, colonna_id='comment_id'):
    """
    Verifica che siano stati rimossi SOLO i duplicati
    """
    print(f" VERIFICA RIMOZIONE DUPLICATI")
    print("=" * 50)
    
    # Carica i dataset
    df_orig = pd.read_csv(file_originale, engine='python', on_bad_lines='skip')
    df_pulito = pd.read_csv(file_pulito, engine='python', on_bad_lines='skip')
    
    print(f" ---> DATASET ORIGINALE:")
    print(f"   > Righe totali: {len(df_orig):,}")
    print(f"   > Duplicati in '{colonna_id}': {df_orig.duplicated(subset=[colonna_id]).sum():,}")
    
    print(f" ---> DATASET PULITO:")
    print(f"   > Righe totali: {len(df_pulito):,}")
    print(f"   > Duplicati rimanenti: {df_pulito.duplicated(subset=[colonna_id]).sum():,}")
    
    # VERIFICA: Controlla che tutti gli ID unici siano preservati
    id_originali = set(df_orig[colonna_id].dropna())
    id_puliti = set(df_pulito[colonna_id].dropna())
    
    id_mancanti = id_originali - id_puliti
    id_aggiunti = id_puliti - id_originali
    
    print(f" VERIFICA ID UNICI:")
    print(f"   > ID unici originali: {len(id_originali):,}")
    print(f"   > ID unici nel pulito: {len(id_puliti):,}")
    print(f"   > ID mancanti (DUPLICATI): {len(id_mancanti):,}")
    print(f"   < ID aggiunti (ERRORE): {len(id_aggiunti):,}")



if __name__ == "__main__":

    input_file = "ds20251031_2102.csv"
    output_file = "dataset/ds_fine.csv"

    #input_file = "dataset/dataset_FINALE_PULITO.csv"
    #output_file = "dataset/dataset_FINALE_PULITO_NO_DUPLICATI.csv"
    #output_file = "prova.csv"

    rimuovi_duplicati_dataset(input_file, output_file)
    verifica_duplicati(input_file, output_file)