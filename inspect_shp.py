import geopandas as gpd

shapefile_path = "small_areas_british_grid.shp"
try:
    gdf = gpd.read_file(shapefile_path)
    print("CRS:", gdf.crs)
    print("Columns:", gdf.columns)
    print("Head:", gdf.head())
except Exception as e:
    print(f"Error: {e}")
