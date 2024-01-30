import geopandas as gpd
from pyogrio import read_dataframe
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
from shapely.geometry import Point

# Global variables
target_parcel = "8818900320"
frontage_type = 1
selected_parcels = []

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
buffer_distance = 0.002
surrounding_parcels = parcel_gdf[parcel_gdf.geometry.buffer(buffer_distance).intersects(target_parcel_df.unary_union)]


def render_map():
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot surrounding parcels
    surrounding_parcels.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.5)

    # Plot Target Parcel
    target_parcel_df.plot(ax=ax, color='red', edgecolor='black')

    # Highlight selected parcels on the map
    if selected_parcels:
        selected_parcels_df = parcel_gdf[parcel_gdf['PIN'].isin(selected_parcels)]
        selected_parcels_df.plot(ax=ax, color='blue', edgecolor='black')

    # Set plot title and labels
    ax.set_title('Parcel of Interest and Surrounding Parcels')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Add Radio Buttons
    radio_ax = plt.axes([0.01, 0.5, 0.1, 0.15])
    radio_buttons = RadioButtons(radio_ax, ('One Frontage', 'Two Frontage'))
    radio_buttons.on_clicked(on_radio_change)

    # Add Confirm button
    confirm_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    confirm_button = Button(confirm_ax, 'Confirm')
    confirm_button.on_clicked(on_confirm)

    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, ax))

    plt.show()
    return ax


def onclick(event, ax):
    if event.xdata is None or event.ydata is None or event.inaxes is None:
        return

    # Convert clicked coordinates to a Shapely Point
    clicked_point = Point(event.xdata, event.ydata)

    # Check which parcels contain the clicked point
    clicked_parcel = parcel_gdf[parcel_gdf.geometry.contains(clicked_point)]

    if not clicked_parcel.empty:
        pin = clicked_parcel.iloc[0]['PIN']
        if pin in selected_parcels:
            selected_parcels.remove(pin)
        else:
            selected_parcels.append(pin)

        # Print the lot size of the clicked parcel
        lot_size = clicked_parcel.iloc[0]['LOTSQFT']
        print(f"Lot size of Parcel {pin}: {lot_size} sq. ft")

    # Update the existing plot
    ax.clear()
    render_map()


def on_radio_change(label):
    global frontage_type
    if label == 'One Frontage':
        frontage_type = 1
    elif label == 'Two Frontage':
        frontage_type = 2


def on_confirm(event):
    plt.close()
    if frontage_type == 2:
        render_map()


# Initial rendering of the map
ax = render_map()
