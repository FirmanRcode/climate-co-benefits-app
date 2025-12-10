import streamlit as st
import pandas as pd
from src.data import load_raw_data, get_area_options, get_unique_benefits, process_area_data
from src.visualizations import (
    plot_projected_benefits_timeline, 
    plot_benefit_breakdown_2050,
    plot_top_areas_comparison,
    plot_time_lapse,
    plot_heatmap_year_benefit,
    plot_motion_bubble_chart
)
from src.map_viz import load_shapefile, plot_choropleth_map

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Climate Co-Benefits Atlas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #00ADB5;
        font-weight: 700;
        font-size: 3rem;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #EEEEEE;
        font-size: 1.5rem;
    }
    .metric-card {
        background-color: #393E46;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #00ADB5;
    }
    .metric-label {
        font-size: 1rem;
        color: #EEEEEE;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def get_data_bundle():
    return load_raw_data()

with st.spinner("Loading Co-Benefits Data..."):
    df_raw, df_lookup = get_data_bundle()

if df_raw.empty:
    st.error("Failed to load data. Please check 'Level_3.xlsx'.")
    st.stop()
    
# Load Shapefile in background
with st.spinner("Loading Map Data..."):
    gdf_uk = load_shapefile()

# --- SIDEBAR ---
st.sidebar.image("https://thedatalab.com/wp-content/uploads/2023/06/The-Data-Lab-Logo-White.png", width=200) # Placeholder or real logo
st.sidebar.title("🌍 Settings")

# Get Options (Name -> Code)
area_options_map = get_area_options(df_lookup, df_raw)
area_display_names = list(area_options_map.keys())

# Find index of Glasgow or Default
default_index = 0
for idx, name in enumerate(area_display_names):
    if "Glasgow" in name:
        default_index = idx
        break

selected_display_name = st.sidebar.selectbox("Select Municipality/Area", area_display_names, index=default_index)
selected_area_code = area_options_map[selected_display_name]

if "E0" in selected_display_name:
    st.sidebar.caption(f"Area Code: {selected_area_code}")

st.sidebar.divider()
st.sidebar.markdown("""
**About this Dashboard:**
This tool empowers local councils to visualize the **co-benefits** of climate action. 
By investing in climate initiatives, you aren't just saving the planet—you are improving **health**, **economy**, and **society**.
""")

# --- MAIN PAGE ---

# Extract pure name for display
display_pure_name = selected_display_name.split('(')[0].strip()

# Header
st.markdown(f'<div class="main-header">Analysis for: {display_pure_name}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">The Hidden Value of Climate Action (2025-2050)</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# PROCESS DATA FOR SELECTED AREA (On-the-fly)
area_df_melted = process_area_data(df_raw, selected_area_code)

if area_df_melted.empty:
    st.warning(f"No data found for area code: {selected_area_code}")
    st.stop()

# Total Benefit 2050
data_2050 = area_df_melted[area_df_melted['Year'] == 2050]
total_benefit_2050 = data_2050['Benefit_Value'].sum()

# Sort by value for Top Benefit
sorted_benefits = data_2050.sort_values('Benefit_Value', ascending=False)

if not sorted_benefits.empty:
    top_benefit_row = sorted_benefits.iloc[0]
    top_benefit_type = top_benefit_row['co-benefit_type']
    top_benefit_val = top_benefit_row['Benefit_Value']
else:
    top_benefit_type = "N/A"
    top_benefit_val = 0

# Key Metrics
col1, col2, col3 = st.columns(3)

def format_currency(val):
    if val >= 1_000_000_000:
        return f"£{val/1_000_000_000:.2f}B"
    elif val >= 1_000_000:
        return f"£{val/1_000_000:.2f}M"
    elif val >= 1_000:
        return f"£{val:,.0f}"
    elif val == 0:
        return "£0"
    else:
        # For small numbers like 0.07
        return f"£{val:,.4f}"

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Projected Benefits (2050)</div>
        <div class="metric-value">{format_currency(total_benefit_2050)}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Top Co-Benefit Driver</div>
        <div class="metric-value">{top_benefit_type}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Contribution of Top Driver</div>
        <div class="metric-value">{format_currency(top_benefit_val)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- VISUALIZATIONS ---

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎬 Time-Lapse", "🗺️ Map"])

with tab1:
    # Row 1: Timeline & Breakdown
    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:
        st.subheader("📈 Trajectory of Growth")
        fig1 = plot_projected_benefits_timeline(area_df_melted, display_pure_name)
        st.plotly_chart(fig1, use_container_width=True)

    with row1_col2:
        st.subheader("🧩 Benefit Composition (2050)")
        fig2 = plot_benefit_breakdown_2050(area_df_melted, display_pure_name)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Row 2: Comparison
    st.subheader("🏆 Contextual Comparison")
    st.write(f"How does {display_pure_name} compare to other top regions?")

    comparison_type = st.selectbox("Compare by Benefit Type", ["Total"] + get_unique_benefits(df_raw))

    if comparison_type == "Total":
        fig3 = plot_top_areas_comparison(df_raw, None)
    else:
        fig3 = plot_top_areas_comparison(df_raw, comparison_type)

    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.header("⏳ Evolution of Benefits (Animation)")
    st.write("Press 'Play' to see how the benefits landscape changes from 2025 to 2050.")
    
    # Toggle between Bar and Bubble
    anim_type = st.radio("Select Animation Style:", ["Bar Race (Ranking)", "Motion Bubble (Value vs Growth)"], horizontal=True)
    
    if anim_type == "Bar Race (Ranking)":
        fig_timelapse = plot_time_lapse(area_df_melted, display_pure_name)
        st.plotly_chart(fig_timelapse, use_container_width=True)
    else:
        st.info("💡 **How to read:** The **X-axis** is the Total Value, **Y-axis** is the Speed of Growth. Bubbles moving UP are accelerating!")
        fig_bubble = plot_motion_bubble_chart(area_df_melted, display_pure_name)
        st.plotly_chart(fig_bubble, use_container_width=True)
    
    st.markdown("### 🔥 Intensity Heatmap")
    fig_heat = plot_heatmap_year_benefit(area_df_melted)
    st.plotly_chart(fig_heat, use_container_width=True)

with tab3:
    st.header("🗺️ Geographic Distribution")
    
    if not gdf_uk.empty:
        col_map_1, col_map_2 = st.columns([3, 1])
        with col_map_1:
            map_benefit = st.selectbox("Select Benefit to Map (2050):", ["Total"] + get_unique_benefits(df_raw))
            fig_map = plot_choropleth_map(gdf_uk, df_raw, map_benefit)
            st.plotly_chart(fig_map, use_container_width=True)
        with col_map_2:
            st.info("Interactive Map Loaded from Shapefile.")
            st.write("This map visualizes the spatial distribution of benefits across the available regions.")
    else:
        st.error("Shapefile could not be loaded.")
