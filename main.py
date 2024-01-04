import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

def read_sensor_data(file_path):
    try:
        # Read the dataset into a dataframe
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{file_path}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Unable to parse the file '{file_path}'. Please check the file format.")
        return None

df = pd.read_csv('GrowLocations.csv')

df = df[(df['Latitude'] >= -90) & (df['Latitude'] <= 90) & (df['Longitude'] >= -180) & (df['Longitude'] <= 180)]

# Remove duplicates based on specific columns
data= df.drop_duplicates(subset=['Latitude', 'Longitude'])

def filter_sensor_data(data):
    # Filter out locations outside the correct bounding box
    filtered_data = data[
        (data['Latitude'] >= -10.592) & (data['Latitude'] <= 1.6848) &
        (data['Longitude'] >= 50.681) & (data['Longitude'] <= 57.985)
        
    ]
    return filtered_data

def create_geo_dataframe(data):
    # Create a GeoDataFrame from the dataframe with coordinates
    geometry = [Point(xy) for xy in zip(data['Latitude'], data['Longitude'])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry, crs='EPSG:4326')
    return gdf

def load_custom_map(map_path):
    try:
        # Load the map image
        map_image = plt.imread(map_path)
        return map_image
    except FileNotFoundError:
        print(f"Error: Map image file '{map_path}' not found.")
        return None

def plot_sensor_locations(gdf, map_image):
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(15, 10))

    # Display the map image using the correct bounding box
    ax.imshow(map_image, extent=[-10.592, 1.6848, 50.681, 57.985])

    # Plotting the sensor locations on the map
    gdf.plot(ax=ax, marker='o', color='red', markersize=5, label='Sensor Locations')

    # Set plot title and labels
    plt.title('Sensor Locations on Custom Map')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')

    # Show the plot
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # File paths
    data_file_path = 'growlocations.csv'
    custom_map_path = 'map7.png'

    # Read and process sensor data
    sensor_data = read_sensor_data(data_file_path)
    if sensor_data is not None:
        filtered_sensor_data = filter_sensor_data(sensor_data)
        geo_dataframe = create_geo_dataframe(filtered_sensor_data)

        # Load the custom map and plot
        custom_map = load_custom_map(custom_map_path)
        if custom_map is not None:
            plot_sensor_locations(geo_dataframe, custom_map)
