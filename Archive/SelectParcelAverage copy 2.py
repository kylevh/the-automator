import geopandas as gpd
from pyogrio import read_dataframe
import matplotlib.pyplot as plt
from shapely.geometry import Point

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


# Define function to handle mouse clicks
click_buffer_distance = .0001
def onclick(event):
    if event.xdata is None or event.ydata is None:
        return

    # Print coordinates of the clicked point
    print(f"Clicked coordinates: ({event.xdata}, {event.ydata})")

    # Convert clicked coordinates to a Shapely Point
    clicked_point = Point(event.xdata, event.ydata)

    # Check which parcels contain the clicked point
    selected_parcels = parcel_gdf[parcel_gdf.geometry.contains(clicked_point)]
    
    # Print information about selected parcels
    if not selected_parcels.empty:
        print("Selected parcels:")
        for index, row in selected_parcels.iterrows():
            print(f"- PIN: {row['PIN']}")
    else:
        print("No parcels selected.")

    # Highlight the selected parcels on the map
    ax.clear()
    surrounding_parcels.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.5)
    target_parcel_df.plot(ax=ax, color='red', edgecolor='black')
    selected_parcels.plot(ax=ax, color='blue', edgecolor='black')  # Highlight selected parcels
    ax.set_title('Parcel of Interest and Surrounding Parcels')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.draw()

# Plot and Render the parcel map
print("Plotting...")
fig, ax = plt.subplots(figsize=(10, 8))

# Plot surrounding parcels
surrounding_parcels.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.5)

# Plot Target Parcel
target_parcel_df.plot(ax=ax, color='red', edgecolor='black')

# Set plot title and labels
ax.set_title('Parcel of Interest and Surrounding Parcels')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()