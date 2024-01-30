from pyogrio import read_dataframe
import geopandas as gpd
import pandas as pd
import time
import matplotlib.pyplot as plt
from parcel_selector import retrieve_parcels

read_start = time.process_time()
#-----------------------------------

# target parcels
target_parcels = ["3364900040", "9528103735", "9528104790"]

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


def FindIntersectionsOnParcel(target_df):
        overlap_found = False
        for name, path in shapefile_paths.items():
            # Skip if checking overlap of 'Parcel' on 'Parcel'
            if name == 'parcel':
                continue

            # print(f"DEBUG: Checking overlap with {name} on parcel {target_parcel}...")

            # Check for intesection with each dataset
            intersecting_features = gpd.overlay(target_df, gdfs[name], how='intersection')

            # Print whether or not there is overlap
            if not intersecting_features.empty:
                overlap_found = True
                print(f"---: {name}.")
        
        if overlap_found:
             print("+ OVERLAP DETECTED")
        else:
             print("- NO OVERLAP DETECTED")


for target_parcel_id in target_parcels:
    # Find target parcel
    target_parcel_df = parcel_gdf[parcel_gdf['PIN'] == target_parcel_id]
    print(f"Target Parcel: {target_parcel_id}")

    # Print out lot size and zoning 'PIN', "ADDR_FULL", "LOTSQFT", "KCA_ZONING",
    lot_size = parcel_gdf.loc[parcel_gdf['PIN'] == target_parcel_id, 'LOTSQFT'].values[0]
    zoning = parcel_gdf.loc[parcel_gdf['PIN'] == target_parcel_id, 'KCA_ZONING'].values[0]
    print(f"Lot Size: {lot_size} - Zoning: {zoning}")

    # Print out all intersections with ECAs
    FindIntersectionsOnParcel(target_parcel_df)

    # Get average of block
    frontage_type, selected_parcels = retrieve_parcels(parcel_gdf, target_parcel_id)
    for parcel in selected_parcels:
         print("Selected Parcel: " + parcel) 

    # Calculate if passes 75/80 rule or note
