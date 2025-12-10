import pandas as pd

file_path = 'Level_3.xlsx'

try:
    # Just read header
    df = pd.read_excel(file_path, nrows=1)
    print("COLUMNS_START")
    for col in df.columns:
        print(col)
    print("COLUMNS_END")
except Exception as e:
    print(f"Error: {e}")
