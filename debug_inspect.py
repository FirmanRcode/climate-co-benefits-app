import pandas as pd

# Load just the first 5 rows
df = pd.read_excel('Level_3.xlsx', nrows=5)

print("COLUMNS:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head().to_string())

print("\nTYPES:")
print(df.dtypes)
