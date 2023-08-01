import requests
import folium
from folium.plugins import AntPath
import time

# Define the location of Mahabaleshwar, Maharashtra, India
location = 'Mahabaleshwar, Maharashtra, India'

# Define the URL for the OpenStreetMap API
url = f'https://nominatim.openstreetmap.org/search?q={location}&format=json'

# Send a GET request to the API
response = requests.get(url)

# Get the latitude and longitude of the location
latitude = float(response.json()[0]['lat'])
longitude = float(response.json()[0]['lon'])

# Define the URL for the Overpass API to search for tourist attractions
overpass_url = 'https://overpass-api.de/api/interpreter'

# Define the Overpass query to search for tourist attractions in Mahabaleshwar
overpass_query = f"""
    [out:json];
    (
      node["tourism"="attraction"]({latitude - 0.1},{longitude - 0.1},{latitude + 0.1},{longitude + 0.1});
      way["tourism"="attraction"]({latitude - 0.1},{longitude - 0.1},{latitude + 0.1},{longitude + 0.1});
      relation["tourism"="attraction"]({latitude - 0.1},{longitude - 0.1},{latitude + 0.1},{longitude + 0.1});
    );
    out center;
    """

# Send a POST request to the Overpass API with the query
response = requests.post(overpass_url, data=overpass_query)

# Get the JSON response and extract the tourist attractions
data = response.json()
attractions = [x['tags']['name:en'] for x in data['elements']]

# Create a folium map centered on Mahabaleshwar
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Add a marker for Mahabaleshwar
folium.Marker([latitude, longitude], popup='Mahabaleshwar', icon=folium.Icon(color='green')).add_to(m)

# Add markers for the tourist attractions
marker_list = []
for element in data['elements']:
    popup_text = element['tags']['name:en'] if 'name:en' in element['tags'] else 'Unnamed Place'
    marker = folium.Marker([element['lat'], element['lon']], popup=popup_text, tooltip=popup_text,
                           icon=folium.Icon(color='red'))
    marker.add_to(m)
    marker_list.append(marker)

# Draw a path connecting all the markers for the tourist attractions
locations = [[marker.location[0], marker.location[1]] for marker in marker_list]
path = AntPath(locations=locations, color='blue', dash_array=[10, 20], delay=800)
path.add_to(m)


# Define a custom function to animate the car marker
def animate_car(marker, locations):
    for location in locations:
        marker.location = location
        time.sleep(0.5)


# Add a car marker that follows the path
car_marker = folium.Marker(location=locations[0], icon=folium.Icon(color='orange', icon='car', prefix='fa'))
car_marker.add_to(m)
animate_car(car_marker, locations)

# Display the map
m.save('map_data/maharashtra_cities_shortest_path_with_places3.html')

# https://towardsdatascience.com/how-to-plot-a-route-on-a-map-fb900a7f6605
# https://mateuszwiza.medium.com/plotting-api-results-on-a-map-using-flask-and-leafletjs-2cf2d3cc660b
