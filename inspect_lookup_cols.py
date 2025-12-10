import pandas as pd

try:
    df = pd.read_excel('lookups.xlsx', nrows=1)
    print("COLS_START")
    for col in df.columns:
        print(col)
    print("COLS_END")
except Exception as e:
    print(f"Error: {e}")
