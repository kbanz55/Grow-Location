import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Read the dataset into a dataframe
data = pd.read_csv('growlocations.csv')

# Filter out locations outside the correct bounding box
data = data[(data['Latitude'] >= -10.592) & (data['Latitude'] <= 1.6848) &
            (data['Longitude'] >= 50.681) & (data['Longitude'] <= 57.985)]

# Create a GeoDataFrame from the dataframe with coordinates
geometry = [Point(xy) for xy in zip(data['Latitude'], data['Longitude'])]  # Swap latitude and longitude
gdf = gpd.GeoDataFrame(data, geometry=geometry, crs='EPSG:4326')

# Load the map image (assuming it's in the same path as the Python file)
map_image = plt.imread('map7.png')

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(15, 10))

# Display the map image using the correct bounding box
ax.imshow(map_image, extent=[-10.592, 1.6848, 50.681, 57.985])

# Plotting the sensor locations on the map
gdf.plot(ax=ax, marker='o', color='red', markersize=5, label='Sensor Locations')

# Set plot title and labels
plt.title('Sensor Locations on Custom Map')
plt.xlabel('Latitude')  # Swap x and y axis labels
plt.ylabel('Longitude')

# Show the plot
plt.legend()
plt.show()