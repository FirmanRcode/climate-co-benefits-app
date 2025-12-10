import geopandas as gpd
import plotly.express as px
import pandas as pd
import streamlit as st
import json

GEOJSON_PATH = "small_areas.geojson"

@st.cache_data
def load_shapefile():
    """
    Loads the GeoJSON file.
    """
    try:
        # Load GeoJSON using geopandas
        gdf = gpd.read_file(GEOJSON_PATH)
        return gdf
    except Exception as e:
        st.error(f"Error loading map: {e}")
        return gpd.GeoDataFrame()

def plot_choropleth_map(gdf, df_data, selected_benefit="Total"):
    """
    Plots a Choropleth map using GeoJSON.
    """
    # Prepare Data: Aggregate by Area
    target_year = 2050
    year_col = target_year if target_year in df_data.columns else str(target_year)
    
    if selected_benefit and selected_benefit != "Total":
        df_filtered = df_data[df_data['co-benefit_type'] == selected_benefit]
    else:
         # Sum all benefits for the area
        df_filtered = df_data
    
    # Group by small_area
    df_sums = df_filtered.groupby('small_area')[year_col].sum().reset_index()
    df_sums.rename(columns={year_col: 'Benefit_Value'}, inplace=True)
    
    # Merge with GeoDataFrame
    # gdf key: 'small_area' (based on inspection)
    gdf_merged = gdf.merge(df_sums, on='small_area', how='left')
    gdf_merged['Benefit_Value'] = gdf_merged['Benefit_Value'].fillna(0)
    
    # Set CRS to WGS84 just in case, though it should be already
    if gdf_merged.crs != "EPSG:4326":
         gdf_merged = gdf_merged.to_crs("EPSG:4326")
    
    fig = px.choropleth_mapbox(
        gdf_merged,
        geojson=gdf_merged.geometry,
        locations=gdf_merged.index,
        color='Benefit_Value',
        hover_name='small_area',
        hover_data=['Benefit_Value'],
        color_continuous_scale="Viridis",
        mapbox_style="carto-darkmatter",
        center={"lat": 54.5, "lon": -2.0}, # UK Center
        zoom=5,
        title=f"Geographic Distribution of Benefits ({selected_benefit}, 2050)"
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        font=dict(family="Inter, sans-serif")
    )
    
    return fig
