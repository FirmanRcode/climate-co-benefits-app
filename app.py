import streamlit as st
import pandas as pd
from src.data import (
    load_lookups, 
    get_area_options, 
    get_area_data, 
    process_area_data_from_df,
    get_unique_benefits,
    get_top_areas_data
)
from src.visualizations import (
    plot_projected_benefits_timeline, 
    plot_benefit_breakdown_2050,
    plot_top_areas_comparison,
    plot_time_lapse,
    plot_heatmap_year_benefit,
    plot_motion_bubble_chart,
    plot_benefit_rose_chart,
    plot_benefit_sankey
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
        color: #555555;
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
    
    /* Animation Keyframes */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING (LAZY) ---
with st.spinner("Initializing..."):
    df_lookup = load_lookups()

# --- IMPORTS FOR MOTION VIZ ---
from streamlit_lottie import st_lottie
import json

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load Lottie Animation (Local)
lottie_json = None
try:
    lottie_json = load_lottiefile("assets/lottie_nature.json")
except Exception as e:
    print(f"Lottie not found: {e}")

# --- SIDEBAR ---
with st.sidebar:
    if lottie_json:
        st_lottie(lottie_json, height=150, key="sidebar_anim")
    st.image("https://thedatalab.com/wp-content/uploads/2023/06/The-Data-Lab-Logo-White.png", width=200)
    st.title("🌍 Settings")

    # Get Options
    area_options_map = get_area_options(df_lookup)

    if not area_options_map:
        st.error("No area options found. Check 'lookups.xlsx'.")
        st.stop()

    area_display_names = list(area_options_map.keys())

    # Default Selection
    default_index = 0
    for idx, name in enumerate(area_display_names):
        if "Glasgow" in name:
            default_index = idx
            break

    selected_display_name = st.selectbox("Select Municipality/Area", area_display_names, index=default_index)
    selected_area_code = area_options_map[selected_display_name]

    if "E0" in selected_display_name:
        st.caption(f"Area Code: {selected_area_code}")

    st.divider()
    st.markdown("""
    **About this Dashboard:**
    This tool empowers local councils to visualize the **co-benefits** of climate action. 
    By investing in climate initiatives, you aren't just saving the planet—you are improving **health**, **economy**, and **society**.
    """)

# --- MAIN PAGE ---

display_pure_name = selected_display_name.split('(')[0].strip()

st.markdown(f'<div class="main-header">Analysis for: {display_pure_name}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">The Hidden Value of Climate Action (2025-2050)</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# FILTER FOR METRICS
col_filter, _ = st.columns([1, 3])
with col_filter:
    metric_year = st.slider("Select Year for Overview:", min_value=2025, max_value=2050, value=2050)

# LOAD SPECIFIC AREA DATA (DuckDB)
area_df_raw = get_area_data(selected_area_code)
area_df_melted = process_area_data_from_df(area_df_raw)

if area_df_melted.empty:
    st.warning(f"No data found for area code: {selected_area_code}")
    st.stop()

# Total Benefit (Dynamic Year)
data_year = area_df_melted[area_df_melted['Year'] == metric_year]
total_benefit_year = data_year['Benefit_Value'].sum()

sorted_benefits = data_year.sort_values('Benefit_Value', ascending=False)
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
        return f"£{val:,.4f}"

# --- COUNT-UP VISUALIZATION ---
# (CSS Animation Strategy)

metric_html_1 = f"""
<div class="metric-card" style="animation: fadeIn 1.5s;">
    <div class="metric-label">Total Projected Benefits ({metric_year})</div>
    <div class="metric-value" style="color: #00ADB5;">{format_currency(total_benefit_year)}</div>
</div>
"""

with col1:
    st.markdown(metric_html_1, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="animation: fadeIn 2s;">
        <div class="metric-label">Top Co-Benefit Driver ({metric_year})</div>
        <div class="metric-value" style="color: #00ADB5;">{top_benefit_type}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card" style="animation: fadeIn 2.5s;">
        <div class="metric-label">Contribution of Top Driver</div>
        <div class="metric-value" style="color: #00ADB5;">{format_currency(top_benefit_val)}</div>
    </div>
    """, unsafe_allow_html=True)
    
# INSERT CSS ANIMATION DEFINITION
# (Already defined in style block at top)

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
        # st.subheader("🧩 Benefit Composition (2050)")
        # fig2 = plot_benefit_breakdown_2050(area_df_melted, display_pure_name)
        # st.plotly_chart(fig2, use_container_width=True)
        
        # UPGRADE: Using Rose Chart instead of Pie for "Juara" effect
        st.subheader(f"🌹 Benefit Flower")
        
        # User control: Static (Specific Year) or Animation (Bloom)?
        rose_mode = st.toggle("🌺 Animate Bloom (2025-2050)", value=False)
        
        try:
             year_arg = None if rose_mode else metric_year
             fig_rose = plot_benefit_rose_chart(area_df_melted, display_pure_name, year=year_arg)
             st.plotly_chart(fig_rose, use_container_width=True)
        except Exception as e:
             st.error(f"Could not render rose chart: {e}")

    st.markdown("---")
    
    # SANKEY DIAGRAM (Value Flow)
    st.subheader(f"🌊 Value Flow Analysis ({metric_year})")
    st.write("Trace where the economic value originates (Health vs Infrastructure vs Environment).")
    try:
        fig_sankey = plot_benefit_sankey(area_df_melted, display_pure_name, year=metric_year)
        st.plotly_chart(fig_sankey, use_container_width=True)
    except Exception as e:
        st.error(f"Could not render Sankey: {e}")
        
    st.markdown("---")

    # Row 2: Comparison
    st.subheader("🏆 Contextual Comparison")
    st.write(f"How does {display_pure_name} compare to other top regions?")
    
    # Get Unique Benefits for dropdown
    benefits_list = get_unique_benefits() # Uses DuckDB DISTINCT
    comparison_type = st.selectbox("Compare by Benefit Type", ["Total"] + benefits_list)

    if comparison_type == "Total":
        df_top10 = get_top_areas_data(None, 2050)
    else:
        df_top10 = get_top_areas_data(comparison_type, 2050)
        
    # Map Codes to Names for clearer display
    if not df_lookup.empty:
         # Create a map code -> name
        code_to_name = pd.Series(df_lookup.local_authority.values, index=df_lookup.small_area).to_dict()
        df_top10['Display_Name'] = df_top10['small_area'].map(code_to_name).fillna(df_top10['small_area'])
    else:
        df_top10['Display_Name'] = df_top10['small_area']

    # NOTE: plot_top_areas_comparison expects df_wide format. 
    # But now we are passing a pre-aggregated DF with columns [small_area, Benefit_Value].
    # We need to adapt the function calls or the function itself.
    # Actually, simpler to just plot directly here or make a new simple plotter.
    # Let's use internal simple plotting for robustness
    import plotly.express as px
    fig3 = px.bar(
        df_top10.sort_values('Benefit_Value', ascending=True),
        y='Display_Name',
        x='Benefit_Value',
        orientation='h',
        title=f"Top 10 Areas ({'Total' if comparison_type=='Total' else comparison_type}) in 2050",
        template='plotly_dark',
        color='Benefit_Value',
        color_continuous_scale='Viridis',
        hover_data=['small_area']
    )
    fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"))
    
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.header("⏳ Evolution of Benefits (Animation)")
    st.write("Press 'Play' to see how the benefits landscape changes from 2025 to 2050.")
    
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
    st.header("🗺️ Geographic Distribution (Timeline)")
    
    # Load Shapefile (GeoJSON) - Cached
    with st.spinner("Loading Map..."):
        gdf_uk = load_shapefile()

    if not gdf_uk.empty:
        col_map_1, col_map_2 = st.columns([3, 1])
        with col_map_1:
            
            # --- MAP CONTROLS ---
            map_year = st.slider("Select Year", min_value=2025, max_value=2050, value=2050, step=1)
            map_benefit = st.selectbox("Select Benefit to Map:", ["Total"] + benefits_list)
            
            # Fetch Map Data on fly
            if map_benefit == "Total":
                query_map = f"SELECT small_area, SUM(\"{map_year}\") as Benefit_Value FROM 'data_chunks/level_3_part_*.parquet' GROUP BY small_area"
            else:
                 query_map = f"SELECT small_area, \"{map_year}\" as Benefit_Value FROM 'data_chunks/level_3_part_*.parquet' WHERE \"co-benefit_type\" = '{map_benefit}'"
            
            import duckdb
            df_map_data = duckdb.execute(query_map).fetchdf()
            
            # Use the existing plotter. df_map_data has 'Benefit_Value'.
            # Add 'co-benefit_type' col if needed by filter logic in plotter, 
            # OR modify plotter to accept simpler data. (Already modified plotter).
            
            # Add dummy year column if plotter strictly requires it, but we modified plotter to handle 'Benefit_Value' direct.
            # Passing 2050 as benefit value name
            
            fig_map = plot_choropleth_map(gdf_uk, df_map_data.copy(), map_benefit)
            # Update title dynamically for the year
            fig_map.update_layout(title=f"Geographic Distribution of Benefits ({map_benefit}, {map_year})")
            
            st.plotly_chart(fig_map, use_container_width=True)
            
        with col_map_2:
            st.info("Interactive Map.")
            st.markdown(f"**Year:** {map_year}")
            st.markdown(f"**Metric:** {map_benefit}")
            st.write("Using optimized GeoJSON + DuckDB.")
    else:
        st.error("Shapefile could not be loaded.")
