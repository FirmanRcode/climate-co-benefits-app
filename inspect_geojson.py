import geopandas as gpd

try:
    gdf = gpd.read_file("small_areas.geojson")
    print("Columns in GeoJSON:", gdf.columns.tolist())
    print("First few rows:")
    print(gdf.head(3))
except Exception as e:
    print(e)
