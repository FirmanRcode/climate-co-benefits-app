import pandas as pd
import streamlit as st
import os
import glob

LEVEL_3_EXCEL = "Level_3.xlsx"
LEVEL_3_PARQUET = "Level_3.parquet"
DATA_CHUNKS_DIR = "data_chunks"
LOOKUP_FILE = "lookups.xlsx"

@st.cache_data
def load_raw_data():
    """
    Loads the dataset (checking chunks first, then parquet, then excel) and Lookups.
    Returns:
        df_data: The main data (wide format).
        df_lookup: The lookup table (small_area -> local_authority).
    """
    # 1. Load Main Data
    df = pd.DataFrame()
    try:
        # Check for Chunks (Priority for Cloud Deployment)
        chunk_files = glob.glob(f"{DATA_CHUNKS_DIR}/level_3_part_*.parquet")
        if chunk_files:
            dfs = [pd.read_parquet(f) for f in chunk_files]
            df = pd.concat(dfs, ignore_index=True)
            # print("Loaded from Parquet Chunks")
        elif os.path.exists(LEVEL_3_PARQUET):
            df = pd.read_parquet(LEVEL_3_PARQUET)
            # print("Loaded from Single Parquet")
        else:
            df = pd.read_excel(LEVEL_3_EXCEL)
            # print("Loaded from Excel")
            
    except Exception as e:
        st.error(f"Error loading main data: {e}")
        return pd.DataFrame(), pd.DataFrame()

    # 2. Load Lookup Data
    try:
        if os.path.exists(LOOKUP_FILE):
             # Read columns: small_area, local_authority
             df_lookup = pd.read_excel(LOOKUP_FILE, usecols=['small_area', 'local_authority'])
             # Drop duplicates just in case
             df_lookup = df_lookup.drop_duplicates(subset=['small_area'])
        else:
             df_lookup = pd.DataFrame(columns=['small_area', 'local_authority'])
    except Exception as e:
        df_lookup = pd.DataFrame(columns=['small_area', 'local_authority'])
        # Not critical, we can survive without names

    return df, df_lookup

def get_area_options(df_lookup, df_data):
    """
    Returns a dict mapping {Display Name -> small_area code}.
    """
    # Get all unique areas from data
    unique_codes = sorted(df_data['small_area'].dropna().unique().tolist())
    
    if df_lookup.empty:
        # Fallback to codes only
        return {code: code for code in unique_codes}
    
    # Merge to get names
    # Create a map code -> name
    code_to_name = pd.Series(df_lookup.local_authority.values, index=df_lookup.small_area).to_dict()
    
    options = {}
    for code in unique_codes:
        name = code_to_name.get(code, "Unknown")
        display = f"{name} ({code})" if name != "Unknown" else code
        options[display] = code
        
    return options

def get_unique_benefits(df):
    if 'co-benefit_type' in df.columns:
        return sorted(df['co-benefit_type'].dropna().unique().tolist())
    return []

def process_area_data(df, area):
    """
    Filters for a specific area first, THEN melts.
    """
    # 1. Filter
    df_area = df[df['small_area'] == area].copy()
    
    # 2. Year Cols
    year_cols = []
    for col in df_area.columns:
        if isinstance(col, int) and 2025 <= col <= 2050:
            year_cols.append(col)
        elif str(col).isdigit() and 2025 <= int(col) <= 2050:
            year_cols.append(col)
            
    id_vars = [col for col in df_area.columns if col not in year_cols]
    
    df_melted = df_area.melt(
        id_vars=id_vars,
        value_vars=year_cols,
        var_name='Year',
        value_name='Benefit_Value'
    )
    
    df_melted['Year'] = df_melted['Year'].astype(int)
    
    return df_melted
