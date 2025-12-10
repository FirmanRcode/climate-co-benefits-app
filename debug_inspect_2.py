import pandas as pd

# Load first 100 rows
df = pd.read_excel('Level_3.xlsx', nrows=100)

print("--- SMALL AREA SAMPLES ---")
print(df['small_area'].unique()[:5])

print("\n--- 2050 COLUMN STATS ---")
if 2050 in df.columns:
    print(df[2050].describe())
else:
    print("Column 2050 not found via integer access.")
    # Try string
    if '2050' in df.columns:
        print("Column '2050' found as string.")
        print(df['2050'].describe())

print("\n--- SAMPLE ROW ---")
print(df.iloc[0])
