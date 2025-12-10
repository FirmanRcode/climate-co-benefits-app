import pandas as pd

file_path = 'lookups.xlsx'
try:
    df = pd.read_excel(file_path, nrows=5)
    print("COLUMNS:")
    print(df.columns.tolist())
    print("\nSAMPLE DATA:")
    print(df.head().to_string())
except Exception as e:
    print(f"Error: {e}")
