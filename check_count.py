import pandas as pd
from src.data import load_raw_data

try:
    df = load_raw_data()
    unique_areas = df['small_area'].nunique()
    print(f"Unique Areas Count: {unique_areas}")
    print(f"Sample Area Codes: {df['small_area'].unique()[:5]}")
except Exception as e:
    print(f"Error: {e}")
