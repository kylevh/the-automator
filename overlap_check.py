import geopandas as gpd

def is_overlapping(target_parcel_df, parcel_gdf, eca_gdf):
    # Check for intesection with each dataset
    intersecting_features = gpd.overlay(target_parcel_df, eca_gdf, how='intersection')

    # Print whether or not there is overlap
    if not intersecting_features.empty:
        print("::: is_overlapping = true")
        return True
    else :
        print("::: is_overlapping = false")
        return False
    

def is_overlapping_eca(target_parcel_df, parcel_gdf, eca_gdfs):
    overlap_found = False
    for name, gdf in eca_gdfs.items():
        # Skip if checking overlap of 'Parcel' on 'Parcel'
        if name == 'parcel':
            continue

        # print(f"DEBUG: Checking overlap with {name} on parcel {target_parcel}...")

        # Check for intesection with each dataset
        intersecting_features = gpd.overlay(target_parcel_df, gdf[name], how='intersection')

        # Print whether or not there is overlap
        if not intersecting_features.empty:
            overlap_found = True
            print(f"---: {name}.")
    
    if overlap_found:
            print("+ OVERLAP DETECTED")
            return True
    else:
            print("- NO OVERLAP DETECTED")
            return False