import pandas as pd
import numpy as np
import os

PARQUET_FILE = "Level_3.parquet"
OUTPUT_DIR = "data_chunks"

def split_parquet():
    if not os.path.exists(PARQUET_FILE):
        print("Parquet file not found.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("Reading parquet...")
    df = pd.read_parquet(PARQUET_FILE)
    
    # Split into 2 chunks
    chunks = np.array_split(df, 2)
    
    for i, chunk in enumerate(chunks):
        filename = f"{OUTPUT_DIR}/level_3_part_{i}.parquet"
        print(f"Saving {filename}...")
        chunk.to_parquet(filename)
        
    print("Done! Files created in data_chunks/")

if __name__ == "__main__":
    split_parquet()
