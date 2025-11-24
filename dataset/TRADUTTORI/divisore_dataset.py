# divisore_dataset.py
import pandas as pd

def dividi_dataset_in_partizioni(file_path, num_partizioni=10):
    """
    Divide il dataset in partizioni per traduzione parallela
    """
    print(" Caricamento dataset completo...")
    df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')
    
    # Crea cartella per le partizioni
    cartella_partizioni = "TRADUTTORI/subset"
    
    # Calcola dimensione di ogni partizione
    dimensione_partizione = len(df) // num_partizioni
    partizioni = []
    
    print(f"Divisione in {num_partizioni} partizioni...")
    
    for i in range(num_partizioni):
        inizio = i * dimensione_partizione
        fine = (i + 1) * dimensione_partizione if i < num_partizioni - 1 else len(df)
        
        partizione = df.iloc[inizio:fine].copy()
        filename = f"{cartella_partizioni}/partizione_{i+1:02d}_di_{num_partizioni}.csv"
        partizione.to_csv(filename, index=False, encoding='utf-8-sig')
        
        partizioni.append(filename)
        print(f"   • Partizione {i+1}: righe {inizio}-{fine} -> {filename}")
    
    
    return partizioni

if __name__ == "__main__":
    dividi_dataset_in_partizioni("dataset/commenti_italy_processati.csv", num_partizioni=3) 