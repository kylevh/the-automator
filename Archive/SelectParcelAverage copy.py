import geopandas as gpd
from pyogrio import read_dataframe
import matplotlib.pyplot as plt


# Target Parcel
target_parcel = "8818900320"

# Process ShapeFile data
print("Processing ShapeFile...")
parcel_shapefile_path = 'Datasets/parcel_data/parcel_data.shp'
parcel_data = read_dataframe(parcel_shapefile_path)
parcel_gdf = gpd.GeoDataFrame(parcel_data)
parcel_gdf.geometry = parcel_gdf.geometry.buffer(0)
parcel_gdf.sindex

# Set Target Parcel DataFrame
target_parcel_df = parcel_gdf[parcel_gdf['PIN'] == target_parcel]

# Get Surrounding Parcels
buffer_distance = .002
surrounding_parcels = parcel_gdf[parcel_gdf.geometry.buffer(buffer_distance).intersects(target_parcel_df.unary_union)]

# Plot and Render the parcel map
print("Plotting...")
fig, ax = plt.subplots(figsize=(10, 10))

# Plot surrounding parcels
surrounding_parcels.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.5)

# Plot Target Parcel
target_parcel_df.plot(ax=ax, color='red', edgecolor='black')

# Set plot title and labels
ax.set_title('Parcel of Interest and Surrounding Parcels')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Display the plot
print("Taking Input...")
selected_indices = plt.ginput(n=-1, timeout=0)

# Extract the selected polygons
print("Extracting selected polygons...")
selected_polygons = [parcel_gdf.iloc[int(index)].geometry for index in selected_indices]

# Highlight selected polygons
print("Highlighting...")
for index, row in parcel_gdf.iterrows():
    if row in selected_polygons:
        # Plot selected polygons with a different color
        row.geometry.plot(ax=ax, facecolor='red', edgecolor='black')
    else:
        # Plot non-selected polygons
        row.geometry.plot(ax=ax, facecolor='none', edgecolor='black')

# Calculate the average 'LOTSIZE'
print("Calculating Average...")
total_lot_size = sum(selected_polygons['LOTSQFT'])
average_lot_size = total_lot_size / len(selected_polygons)
print("Average LOTSIZE of selected polygons:", average_lot_size)

