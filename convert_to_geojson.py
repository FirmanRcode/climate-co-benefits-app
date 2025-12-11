import geopandas as gpd
import os

shp_path = "small_areas_british_grid.shp"
geojson_path = "small_areas.geojson"

def convert():
    try:
        print("Loading Shapefile...")
        gdf = gpd.read_file(shp_path)
        
        print(f"Original CRS: {gdf.crs}")
        
        # Reproject to WGS84
        print("Reprojecting to EPSG:4326...")
        gdf = gdf.to_crs("EPSG:4326")
        
        # ULTRA AGGRESSIVE SIMPLIFICATION
        # Target: < 5MB file size
        # 0.02 degrees ~ 2km precision. Good enough for national view.
        print("Simplifying geometries (Aggressive)...")
        gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.02, preserve_topology=False)
        
        print(f"Saving to {geojson_path}...")
        gdf.to_file(geojson_path, driver='GeoJSON')
        print("Conversion Complete!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    convert()
