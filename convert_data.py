import pandas as pd
import time
import os

excel_file = 'Level_3.xlsx'
parquet_file = 'Level_3.parquet'

print(f"[{time.strftime('%H:%M:%S')}] Starting conversion...")

if os.path.exists(parquet_file):
    print(f"[{time.strftime('%H:%M:%S')}] {parquet_file} already exists. Deleting to regenerate.")
    os.remove(parquet_file)

try:
    print(f"[{time.strftime('%H:%M:%S')}] Reading Excel file (this takes memory and time)...")
    # Using openpyxl engine explicitly, though it's default for xlsx
    df = pd.read_excel(excel_file, engine='openpyxl')
    print(f"[{time.strftime('%H:%M:%S')}] Excel read complete. Rows: {len(df)}")
    
    print(f"[{time.strftime('%H:%M:%S')}] Saving to Parquet...")
    df.to_parquet(parquet_file)
    print(f"[{time.strftime('%H:%M:%S')}] SUCCESS: Saved to {parquet_file}")
    
except Exception as e:
    print(f"[{time.strftime('%H:%M:%S')}] ERROR: {e}")
