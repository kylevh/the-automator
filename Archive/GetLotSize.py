import geopandas as gpd

# Load the shapefile into a GeoDataFrame
shapefile_path = "path_to_your_shapefile.shp"
gdf = gpd.read_file(shapefile_path)

# Specify the parcel ID you want to retrieve the lot size for
parcel_id = "your_specified_parcel_id"

# Query the GeoDataFrame to retrieve the lot size for the specified parcel ID
lot_size = gdf.loc[gdf['parcel_id_column_name'] == parcel_id, 'lot_size_column_name'].values[0]

print("Lot Size of Parcel", parcel_id, "is", lot_size)