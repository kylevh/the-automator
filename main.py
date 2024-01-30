from parcel_selector import retrieve_parcels
from pyogrio import read_dataframe
import geopandas as gpd
import pandas as pd
import time
import matplotlib.pyplot as plt

# target parcels
target_parcels = ["9528103735", "3364900040", "9528104790"]

# shapefile path
shapefile_paths = {
    'parcel' : 'Datasets/parcel_data/parcel_data.shp',
    'steep_slope' : 'Datasets/ECA_Steep_Slope/ECA_Steep_Slope.shp',
    'liquefaction' : 'Datasets/ECA_Liquefaction_Prone_Areas/ECA_Liquefaction_Prone_Areas.shp',
}

# Read each shapefile path into DataFrame
gdfs = {}
for name, path in shapefile_paths.items():
    print(f"DEBUG: Processing {name} shapefile into GeoDataFrame...")
    data = read_dataframe(path)
    gdf = gpd.GeoDataFrame(data)
    print(f"DEBUG: Buffering {name} GDF...")
    gdf.geometry = gdf.geometry.buffer(0)
    gdfs[name] = gdf
    print(f"DEBUG: Indexing {name} GDF...")
    gdfs[name].sindex 

# Declare each GeoDataFrame by name
parcel_gdf = gdfs['parcel']
# steep_slope_gdf = gdfs['steep_slope']

