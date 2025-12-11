import pandas as pd
import streamlit as st
import os
import glob
import duckdb

DATA_CHUNKS_DIR = "data_chunks"
LOOKUP_FILE = "lookups.xlsx"
PARQUET_PATTERN = f"{DATA_CHUNKS_DIR}/level_3_part_*.parquet"

@st.cache_data
def load_lookups():
    """
    Loads ONLY the lookup table (Small, safe for memory).
    """
    try:
        if os.path.exists(LOOKUP_FILE):
             df_lookup = pd.read_excel(LOOKUP_FILE, usecols=['small_area', 'local_authority'])
             df_lookup = df_lookup.drop_duplicates(subset=['small_area'])
             return df_lookup
    except Exception as e:
        st.error(f"Error loading lookups: {e}")
    return pd.DataFrame(columns=['small_area', 'local_authority'])

def get_area_options(df_lookup):
    """
    Returns a dict mapping {Display Name -> small_area code}.
    Uses the lookup dataframe.
    """
    if df_lookup.empty:
        return {}
    
    # Create a map code -> name
    code_to_name = pd.Series(df_lookup.local_authority.values, index=df_lookup.small_area).to_dict()
    
    # We need a list of ALL valid area codes.
    # To avoid scanning the big file, we assume the lookup covers most.
    # OR we can do a distinct query on parquet if needed, but lookups is faster.
    
    options = {}
    # Sort by name
    sorted_items = sorted(code_to_name.items(), key=lambda x: str(x[1]))
    
    for code, name in sorted_items:
        display = f"{name} ({code})"
        options[display] = code
        
    return options

def get_area_data(area_code):
    """
    Fetches rows for a specific area using DuckDB (Low Memory).
    """
    query = f"SELECT * FROM '{PARQUET_PATTERN}' WHERE small_area = ?"
    try:
        # Use duckdb to query parquet directly without loading into pandas first
        df = duckdb.execute(query, [area_code]).fetchdf()
        return df
    except Exception as e:
        st.error(f"Error reading data for {area_code}: {e}")
        return pd.DataFrame()

def get_unique_benefits(sample_df=None):
    """
    Returns unique co-benefit types.
    Optimization: Hardcode or query once.
    """
    # Hardcoded or efficient query
    # return ["Health", "Job Creation", "Economic", "Social"] # Example
    # Let's query distinct
    query = f"SELECT DISTINCT \"co-benefit_type\" FROM '{PARQUET_PATTERN}'"
    try:
        df = duckdb.execute(query).fetchdf()
        return sorted(df['co-benefit_type'].tolist())
    except:
        return []

def get_top_areas_data(benefit_type=None, year=2050):
    """
    Get top 10 areas for a specific benefit/year.
    """
    col_name = str(year)
    
    if benefit_type:
        query = f"""
            SELECT small_area, "{year}" as Benefit_Value
            FROM '{PARQUET_PATTERN}'
            WHERE "co-benefit_type" = ?
            ORDER BY "{year}" DESC
            LIMIT 10
        """
        params = [benefit_type]
    else:
        # Aggregate ALL benefits
        query = f"""
            SELECT small_area, SUM("{year}") as Benefit_Value
            FROM '{PARQUET_PATTERN}'
            GROUP BY small_area
            ORDER BY Benefit_Value DESC
            LIMIT 10
        """
        params = []
        
    try:
        df = duckdb.execute(query, params).fetchdf()
        # Add 'co-benefit_type' col for consistency in plotting if needed
        # df['co-benefit_type'] = benefit_type if benefit_type else "Total"
        return df
    except Exception as e:
        st.error(f"Error fetching top areas: {e}")
        return pd.DataFrame()

def process_area_data_from_df(df_area):
    """
    Melts the single-area dataframe.
    """
    if df_area.empty:
        return pd.DataFrame()

    # Smart Melt
    # identify numeric columns that look like years
    cols = df_area.columns
    year_cols = []
    for col in cols:
        # Check if column name is exactly a year string or int
        if str(col).isdigit() and 2025 <= int(col) <= 2050:
             year_cols.append(col)
             
    id_vars = [c for c in cols if c not in year_cols]
    
    df_melted = df_area.melt(
        id_vars=id_vars,
        value_vars=year_cols,
        var_name='Year',
        value_name='Benefit_Value'
    )
    
    df_melted['Year'] = df_melted['Year'].astype(int)
    return df_melted
