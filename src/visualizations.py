import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

PINK = "#FF2E63"
CYAN = "#08D9D6"
DARK_BG = "#222831"

def plot_projected_benefits_timeline(df_melted, area):
    """
    Line chart showing the total benefits over time for a specific area.
    df_melted: Already filtered for the specific area.
    """
    if df_melted.empty:
        return go.Figure()

    grouped = df_melted.groupby(['Year', 'co-benefit_type'])['Benefit_Value'].sum().reset_index()
    
    fig = px.area(
        grouped, 
        x='Year', 
        y='Benefit_Value', 
        color='co-benefit_type',
        title=f"Projected Benefits Growth (2025-2050)",
        template='plotly_dark'
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Benefit Value (£)",
        legend_title="Co-Benefit Type",
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def plot_benefit_breakdown_2050(df_melted, area):
    """
    Bar chart showing the breakdown of benefits in 2050.
    """
    # Filter for 2050
    data_2050 = df_melted[df_melted['Year'] == 2050]
    
    if data_2050.empty:
        return go.Figure()

    grouped = data_2050.groupby('co-benefit_type')['Benefit_Value'].sum().reset_index()
    grouped = grouped.sort_values('Benefit_Value', ascending=True) # For H bar
    
    fig = px.bar(
        grouped,
        y='co-benefit_type',
        x='Benefit_Value',
        orientation='h',
        title=f"Co-Benefits Composition in 2050",
        color='Benefit_Value',
        color_continuous_scale=px.colors.sequential.Teal,
        template='plotly_dark'
    )
    
    fig.update_layout(
        xaxis_title="Total Value",
        yaxis_title="",
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def plot_top_areas_comparison(df_wide, benefit_type=None):
    """
    Compares top 10 areas for total benefits (accumulated or 2050).
    df_wide: The raw wide dataframe (not melted).
    """
    # Use the helper function effectively here or just do logic
    # We need to process the wide dataframe.
    
    target_year = 2050
    col_name = target_year
    if col_name not in df_wide.columns:
        col_name = str(target_year)
        
    if col_name not in df_wide.columns:
        return go.Figure()
        
    df_year = df_wide[['small_area', 'co-benefit_type', col_name]].copy()
    
    if benefit_type:
        df_year = df_year[df_year['co-benefit_type'] == benefit_type]
    
    grouped = df_year.groupby('small_area')[col_name].sum().reset_index()
    grouped.rename(columns={col_name: 'Benefit_Value'}, inplace=True)
    
    top_10 = grouped.sort_values('Benefit_Value', ascending=False).head(10)
    top_10 = top_10.sort_values('Benefit_Value', ascending=True) # Sort for plot
    
    fig = px.bar(
        top_10,
        y='small_area',
        x='Benefit_Value',
        orientation='h',
        title=f"Top 10 Areas ({'Total' if not benefit_type else benefit_type}) in {target_year}",
        color='Benefit_Value',
        color_continuous_scale=px.colors.sequential.Viridis,
        template='plotly_dark'
    )
    
    fig.update_layout(
        xaxis_title="Value",
        yaxis_title="",
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def plot_time_lapse(df_melted, area):
    """
    Animated Bar Chart showing how benefits change over time.
    """
    if df_melted.empty:
        return go.Figure()
        
    # We want to see how the 'co-benefit_type' ranking changes over years
    # Group by Year and Type
    grouped = df_melted.groupby(['Year', 'co-benefit_type'])['Benefit_Value'].sum().reset_index()
    
    # Sort for better animation stability
    grouped = grouped.sort_values(['Year', 'Benefit_Value'], ascending=[True, True])
    
    fig = px.bar(
        grouped,
        x="Benefit_Value",
        y="co-benefit_type",
        animation_frame="Year",
        orientation='h',
        range_x=[0, grouped['Benefit_Value'].max() * 1.1], # Fix x-axis range
        title=f"Evolution of Co-Benefits (2025-2050)",
        color="co-benefit_type",
        template='plotly_dark'
    )
    
    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        updatemenus=[dict(type='buttons', showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])])]
    )
    
    return fig

def plot_heatmap_year_benefit(df_melted):
    """
    Heatmap of Benefits vs Years.
    """
    if df_melted.empty:
        return go.Figure()
        
    grouped = df_melted.groupby(['Year', 'co-benefit_type'])['Benefit_Value'].sum().reset_index()
    
    fig = px.density_heatmap(
        grouped,
        x="Year",
        y="co-benefit_type",
        z="Benefit_Value",
        title="Heatmap: Intensity of Benefits over Time",
        color_continuous_scale="Viridis",
        template='plotly_dark'
    )
    
    fig.update_layout(
         font=dict(family="Inter, sans-serif"),
         plot_bgcolor="rgba(0,0,0,0)",
         paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def plot_motion_bubble_chart(df_melted, area):
    """
    Gapminder-style Bubble Chart:
    X = Total Benefit Value
    Y = Growth (Year-over-Year Change)
    Size = Total Benefit Value
    Animation = Year
    """
    if df_melted.empty:
        return go.Figure()
        
    df = df_melted.copy()
    df.sort_values(['co-benefit_type', 'Year'], inplace=True)
    
    # Calculate Growth (Absolute Change)
    df['Growth'] = df.groupby('co-benefit_type')['Benefit_Value'].diff().fillna(0)
    
    # Filter out 2025 (start year has 0 growth usually) to avoid confusion, or keep it.
    
    # FIX: Plotly size cannot be negative.
    df['Size'] = df['Benefit_Value'].clip(lower=0)
    
    fig = px.scatter(
        df,
        x="Benefit_Value",
        y="Growth",
        animation_frame="Year",
        animation_group="co-benefit_type",
        size="Size", # Use value clipped to 0
        color="co-benefit_type",
        hover_name="co-benefit_type",
        hover_data={"Size": False, "Benefit_Value": ":.4f", "Growth": ":.4f"},
        title=f"Dynamics: Value vs. Growth Speed ({area})",
        template='plotly_dark',
        size_max=55,
        range_x=[df['Benefit_Value'].min() * 1.1, df['Benefit_Value'].max() * 1.1],
        range_y=[df['Growth'].min() * 1.1, df['Growth'].max() * 1.1]
    )
    
    fig.update_layout(
        xaxis_title="Total Value (£)",
        yaxis_title="Yearly Growth (£)",
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
         updatemenus=[dict(type='buttons', showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])])]
    )
    
    return fig

    return fig

def plot_benefit_rose_chart(df, area_name, year=None):
    """
    Plots a Nightingale Rose Chart (Polar Bar).
    If year is None, it animates from 2025 to 2050 (Bloom Effect).
    If year is specific, it shows static.
    """
    # Filter POSITIVE values only
    df_clean = df[df['Benefit_Value'] > 0].copy()
    
    # Clean Labels
    df_clean['Display_Label'] = df_clean['co-benefit_type'].str.replace('_', ' ').str.title()
    
    if year:
        # Static Mode
        df_plot = df_clean[df_clean['Year'] == year]
        title_text = f"The 'Flower' of Benefits in {year}"
        anim_args = {}
    else:
        # Animation Mode
        df_plot = df_clean.sort_values("Year")
        title_text = f"The Blooming Benefits (2025-2050)"
        anim_args = {
            "animation_frame": "Year",
            "range_r": [0, df_clean['Benefit_Value'].max() * 1.1] # Fix scale so it grows
        }
    
    # Sort for petal organization
    df_plot = df_plot.sort_values(['Year', 'Benefit_Value'], ascending=[True, False])

    fig = px.bar_polar(
        df_plot,
        r="Benefit_Value",
        theta="Display_Label",
        color="Benefit_Value",
        template="plotly_dark",
        color_continuous_scale="Viridis",
        title=title_text,
        hover_data={"Display_Label": True, "Benefit_Value": ":.4f"},
        **anim_args
    )
    
    # Add Play Button if animating
    updatemenus = []
    if not year:
        updatemenus = [dict(type='buttons', showactive=False,
            buttons=[dict(label='▶️ Bloom',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])])]

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=False),
            angularaxis=dict(tickfont=dict(size=12, color="#EEE"))
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        updatemenus=updatemenus
    )
    
    return fig

def plot_benefit_sankey(df, area_name, year=2050):
    """
    Sankey Diagram with High Contrast/Neon Colors.
    """
    df_year = df[df['Year'] == year].copy()
    
    if df_year.empty:
        return go.Figure()

    categories = {
        'Health': ['physical_activity', 'diet_change', 'dampness', 'excess_cold', 'excess_heat'],
        'Infrastructure': ['congestion', 'road_safety', 'road_repairs', 'hassle_costs'],
        'Environment': ['air_quality', 'noise']
    }
    
    benefit_to_cat = {}
    for cat, benefits in categories.items():
        for b in benefits:
            benefit_to_cat[b] = cat
            
    cat_list = list(categories.keys())
    benefit_list = df_year['co-benefit_type'].unique().tolist()
    all_labels = cat_list + benefit_list
    label_to_idx = {lbl: i for i, lbl in enumerate(all_labels)}
    
    sources = []
    targets = []
    values = []
    colors = []
    
    # HIGH CONTRAST NEON PALETTE
    cat_colors = {
        'Health': '#FF0055',       # Neon Red/Pink
        'Infrastructure': '#00F0FF', # Cyan/Electric Blue
        'Environment': '#CCFF00'     # Lime Green
    }

    def hex_to_rgba(hex_code, opacity=0.8): # Increased opacity for visibility
        h = hex_code.lstrip('#')
        try:
            rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {opacity})"
        except:
             return f"rgba(255, 255, 255, {opacity})"

    for _, row in df_year.iterrows():
        benefit = row['co-benefit_type']
        val = row['Benefit_Value']
        cat = benefit_to_cat.get(benefit, 'Other')
        
        if val > 0:
            sources.append(label_to_idx[cat])
            targets.append(label_to_idx[benefit])
            values.append(val)
            base_color = cat_colors.get(cat, '#FFFFFF')
            colors.append(hex_to_rgba(base_color, 0.6)) # Link opacity
            
    # Node Colors (Matches Links but Solid)
    node_colors = []
    for lbl in all_labels:
        # Determine category of the node
        if lbl in cat_colors:
            node_colors.append(cat_colors[lbl])
        else:
            # It's a benefit node, find its category
            parent_cat = benefit_to_cat.get(lbl, 'Other')
            node_colors.append(cat_colors.get(parent_cat, '#888'))

    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 20,
          thickness = 25,
          line = dict(color = "white", width = 1), # White outline for pop
          label = [l.replace('_',' ').title() for l in all_labels],
          color = node_colors # Explicit colorful nodes
        ),
        link = dict(
          source = sources,
          target = targets,
          value = values,
          color = colors
        ))])

    fig.update_layout(
        title_text=f"Value Flow Analysis ({year})", 
        font=dict(family="Inter", size=14, color="white"), # Bigger white text
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        template='plotly_dark'
    )
    return fig
