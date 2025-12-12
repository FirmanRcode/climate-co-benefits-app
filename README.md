# 🌍 Climate Co-Benefits Dashboard (The Hidden Value of Climate Action)

![Status](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-ff4b4b)

> **"Unveiling the monetary value of climate action beyond just carbon reduction."**

This interactive dashboard visualizes the **co-benefits** of climate policies (such as improved air quality, health, and infrastructure) across various municipalities in the UK (Glasgow, etc.). It uses advanced data storytelling techniques to make complex economic data accessible and engaging.

## ✨ Key Features (The "Juara" Visuals)

### 1. 🌺 Animated Nightingale Rose Chart ("The Flower of Benefits")
*   **Concept**: Visualizes the 11 co-benefit types as petals of a flower.
*   **Interaction**: Includes a "Bloom" animation that evolves from 2025 to 2050.
*   **Tech**: Plotly Polar Bar Charts with animation frames.

### 2. 🌊 Neon Sankey Diagram ("Value Flow Analysis")
*   **Concept**: Traces how broad categories (Health, Infrastructure, Environment) flow into specific monetary benefits.
*   **Style**: High-contrast Neon aesthetics for maximum readability on dark mode.

### 3. 🏎️ Emoji Race (Motion Bubble Chart)
*   **Concept**: A playful twist on the Gapminder chart. Instead of dots, **Emojis** (🏃, 💨, 🚦) themselves race across the screen!
*   **Axes**: X = Total Value, Y = Growth Speed.

### 4. ⏳ Time-Lapse Bar Race
*   **Concept**: A "Racing Bar Chart" showing how different benefits overtake each other in ranking over the 25-year period.

### 5. 🗺️ Interactive Geospatial Map
*   **Data**: High-resolution GeoJSON integration for distinct small areas (Data Zones).
*   **Control**: Dynamic Time-Slider to see spatial evolution.

### 6. 💡 Interactive Benefit Explorer
*   **UI**: A "Living Icon" grid where users can hover over animated stickers to understand each benefit category instantly.
*   **Lottie**: Integrated specific "Money Growth" animations to symbolize economic potential.

## 🛠️ Technology Stack

*   **Core**: [Streamlit](https://streamlit.io/) (Python)
*   **Visualization**: [Plotly Express & Graph Objects](https://plotly.com/python/)
*   **Data Engine**: [DuckDB](https://duckdb.org/) (High-performance in-memory SQL for Parquet/GeoJSON)
*   **Spatial**: GeoPandas, Shapely
*   **Animation**: Streamlit Lottie

## 🚀 Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/FirmanRcode/climate-co-benefits-app.git
    cd climate-co-benefits-app
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

```
├── app.py                # Main Application Entry Point
├── src/
│   ├── data.py           # DuckDB Data Loader & Caching logic
│   ├── visualizations.py # All Plotly Chart functions (Rose, Sankey, Map, etc.)
│   └── map_viz.py        # Geospatial rendering logic
├── assets/               # Lottie JSONs and Static Images
├── data/                 # Parquet and GeoJSON files (not always in repo)
└── requirements.txt      # Python dependencies
```

## 📧 Contact & Credits

**Developed by**: Restu Firmansyah
**Goal**: Visual Data Science Competition Entry / Portfolio

---
*Created with ❤️ and a lot of ☕*
