import pandas as pd
import sys

# Redirect output to file
with open('debug_output.txt', 'w') as f:
    sys.stdout = f
    
    try:
        df = pd.read_excel('Level_3.xlsx', nrows=50)
        
        print("=== COLUMNS ===")
        print(df.columns.tolist())
        
        print("\n=== SMALL AREA (First 10 Unique) ===")
        print(df['small_area'].unique()[:10])
        
        print("\n=== 2050 VALUES (Head) ===")
        print(df[2050].head())
        
        print("\n=== 2050 STATS ===")
        print(df[2050].describe())
        
        print("\n=== ROW 0 FULL ===")
        print(df.iloc[0])
        
    except Exception as e:
        print(f"ERROR: {e}")
