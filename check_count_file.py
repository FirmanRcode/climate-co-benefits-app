import pandas as pd
from src.data import load_raw_data

try:
    df = load_raw_data()
    unique_areas = df['small_area'].nunique()
    result = f"Count: {unique_areas}\nSample: {df['small_area'].unique()[:5]}"
    with open("count.txt", "w") as f:
        f.write(result)
    print("Done")
except Exception as e:
    with open("count.txt", "w") as f:
        f.write(f"Error: {e}")
