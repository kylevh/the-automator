from parcel_selector import retrieve_parcels
from pyogrio import read_dataframe
import geopandas as gpd
import pandas as pd
import time
import matplotlib.pyplot as plt

from overlap_check import is_overlapping, is_overlapping_eca

# target parcels
target_parcels = ["8823901695", "9528103735", "3364900040", "9528104790"]

# shapefile path
shapefile_paths = {
    'parcel' : 'Datasets/parcel_data/parcel_data.shp',
    'steep_slope' : 'Datasets/ECA/ECA_Steep_Slope/ECA_Steep_Slope.shp',
    'liquefaction' : 'Datasets/ECA/ECA_Liquefaction_Prone_Areas/ECA_Liquefaction_Prone_Areas.shp',
    'urban_village' : 'Datasets/Layers/Urban_Centers_Villages_and_Manufacturing_Industrial_Centers/Urban_Centers_Villages_and_Manufacturing_Industrial_Centers.shp'
}

# Read each shapefile path into DataFrame
gdfs = {}
for name, path in shapefile_paths.items():
    print(f"::: Processing '{name}' shapefile into GeoDataFrame...")
    data = read_dataframe(path)
    gdf = gpd.GeoDataFrame(data)
    gdf.geometry = gdf.geometry.buffer(0)
    gdfs[name] = gdf
    gdfs[name].sindex 

# Declare each GeoDataFrame by name
parcel_gdf = gdfs['parcel']
# steep_slope_gdf = gdfs['steep_slope']
# liquefaction_gdf = gdfs['liquefaction']

# Can delete later
target_parcel_df = parcel_gdf[parcel_gdf['PIN'] == target_parcels[0]]
is_overlapping(target_parcel_df, parcel_gdf, gdfs['urban_village'])

