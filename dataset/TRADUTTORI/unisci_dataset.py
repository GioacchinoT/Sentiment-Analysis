# unisci_partizioni.py
import pandas as pd
import glob
import os

def unisci_partizioni_tradotte():
    """
    Unisce tutte le partizioni tradotte in un unico dataset
    """
    print("Unione partizioni tradotte...")
    
    # Trova tutti i file tradotti
    files_tradotti = glob.glob("TRADUTTORI/ita/*_TRADOTTO.csv")
    
    if not files_tradotti:
        print("Nessun file tradotto trovato!")
        return
    
    print(f"Trovati {len(files_tradotti)} file tradotti")
    
    # Carica e unisci tutti i dataset
    datasets = []
    for file in sorted(files_tradotti):
        print(f"   > Caricamento: {file}")
        df_part = pd.read_csv(file, engine='python')
        datasets.append(df_part)
    
    # Unisci tutto
    df_completo = pd.concat(datasets, ignore_index=True)
    
    # Salva dataset finale
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_file = f"ds{timestamp}.csv"
    
    df_completo.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n--> DATASET COMPLETO CREATO!")
    print(f"   > File: {output_file}")
    print(f"   > Righe: {len(df_completo):,}")
    print(f"   > Dimensioni: {os.path.getsize(output_file) / (1024*1024):.1f} MB")

if __name__ == "__main__":
    unisci_partizioni_tradotte()