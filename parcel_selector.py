import geopandas as gpd
from pyogrio import read_dataframe
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
from shapely.geometry import Point

def retrieve_parcels(parcel_gdf, target_parcel):
    # Frontage Type - Default set to 1
    frontage_type = 1

    # UTM Zone 10T
    projected_crs = 'EPSG:32610'

    # Set Target Parcel DataFrame
    target_parcel_df = parcel_gdf[parcel_gdf['PIN'] == target_parcel]

    # parcel_gdf = parcel_gdf.to_crs(projected_crs)
    # target_parcel_df = target_parcel_df.to_crs(projected_crs)

    # Get Surrounding Parcels
    print("Buffering...")
    buffer_distance = .002
    surrounding_parcels = parcel_gdf[parcel_gdf.geometry.buffer(buffer_distance).intersects(target_parcel_df.unary_union)]
    print("Buffering Done")

    # Define function to handle mouse clicks
    selected_parcels = []

    def onclick(event):
        nonlocal selected_parcels
        if event.xdata is None or event.ydata is None or event.inaxes is None or event.inaxes == radio_ax:
            return

        # Print coordinates of the clicked point
        #print(f"Clicked coordinates: ({event.xdata}, {event.ydata})")

        # Convert clicked coordinates to a Shapely Point
        clicked_point = Point(event.xdata, event.ydata)
        
        # Check which parcels contain the clicked point
        clicked_parcel = parcel_gdf[parcel_gdf.geometry.contains(clicked_point)]
        
        # Check if the clicked parcel is already selected
        if not clicked_parcel.empty:
            pin = clicked_parcel.iloc[0]['PIN']
            if pin in selected_parcels:
                # If parcel is already selected, remove it
                selected_parcels.remove(pin)
            else:
                # If parcel is not selected, add it to the list
                selected_parcels.append(pin)

            # Print the lot size of the clicked parcel
            lot_size = clicked_parcel.iloc[0]['LOTSQFT']
            print(f"Lot size of Parcel {pin}: {lot_size} sq. ft")

        # Highlight the selected parcels on the map
        ax.clear()
        surrounding_parcels.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.5)
        target_parcel_df.plot(ax=ax, color='red', edgecolor='black')
        selected_parcels_df = parcel_gdf[parcel_gdf['PIN'].isin(selected_parcels)]
        selected_parcels_df.plot(ax=ax, color='blue', edgecolor='black')  # Highlight selected parcels
        
        ax.set_title(f"Parcel ID: {target_parcel}")
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        plt.draw()


    def on_radio_change(label):
        global frontage_type
        # This function will be called when the radio button selection changes
        if label == 'One Frontage':
            frontage_type = 1
        elif label == 'Two Frontage' :
            frontage_type = 2

    def on_confirm(event):
        plt.close()

        



    # Plot and Render the parcel map
    print("Plotting...")
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot surrounding parcels
    surrounding_parcels.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.5)

    # Plot Target Parcel
    target_parcel_df.plot(ax=ax, color='red', edgecolor='black')

    # Set plot title and labels
    ax.set_title("Parcel ID: {target_parcel}")
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

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    return frontage_type, selected_parcels

if __name__ == "__main__":
    parcel_shapefile_path = 'Datasets/parcel_data/parcel_data.shp'
    target_parcel = "8818900320"
    # Process ShapeFile data
    print("Processing ShapeFile...")
    parcel_data = read_dataframe(parcel_shapefile_path)
    parcel_gdf = gpd.GeoDataFrame(parcel_data)
    parcel_gdf.geometry = parcel_gdf.geometry.buffer(0)
    parcel_gdf.sindex
    print(retrieve_parcels(parcel_shapefile_path, target_parcel))
