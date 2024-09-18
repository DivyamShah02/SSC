import math
import numpy as np
import requests
import pdb
import random

def generate_coordinates_within_bounds(min_lat, max_lat, min_lon, max_lon, step_size):
    """
    Generate coordinates within a bounding box defined by min_lat, max_lat, min_lon, max_lon.
    
    :param min_lat: Minimum latitude of the bounding box.
    :param max_lat: Maximum latitude of the bounding box.
    :param min_lon: Minimum longitude of the bounding box.
    :param max_lon: Maximum longitude of the bounding box.
    :param step_size: The step size in degrees to generate coordinates.
    :return: A list of tuples representing coordinates within the bounding box.
    """
    latitudes = np.arange(min_lat, max_lat, step_size)
    longitudes = np.arange(min_lon, max_lon, step_size)
    
    coordinates = [(lat, lon) for lat in latitudes for lon in longitudes]
    
    return coordinates

def get_bounds(lat, lon, radius_km):
    """
    Get the bounding box for a given point and radius.
    """
    R = 6371  # Earth radius in kilometers

    # Calculate the bounding box
    lat_radians = math.radians(lat)
    lon_radians = math.radians(lon)
    radius_degrees = radius_km / R * (180 / math.pi)

    min_lat = lat - radius_degrees
    max_lat = lat + radius_degrees

    min_lon = lon - radius_degrees / math.cos(lat_radians)
    max_lon = lon + radius_degrees / math.cos(lat_radians)

    return min_lat, max_lat, min_lon, max_lon

def get_distance(origin_lat, origin_lng, destination_lat, destination_lng, api_key):
    # Define the endpoint for the Distance Matrix API
    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"

    # Parameters for the request
    params = {
        "origins": f"{origin_lat},{origin_lng}",
        "destinations": f"{destination_lat},{destination_lng}",
        "key": api_key,
        "mode": "driving"  # You can change this to "walking", "bicycling", "transit" if needed
    }

    # Make the request to the Google Maps Distance Matrix API
    response = requests.get(endpoint, params=params)

    # Parse the response
    if response.status_code == 200:
        data = response.json()
        if data['rows'][0]['elements'][0]['status'] == 'OK':
            # Extract distance and duration
            distance = data['rows'][0]['elements'][0]['distance']['text']
            duration = data['rows'][0]['elements'][0]['duration']['text']
            return distance, duration
        else:
            return None, "No route found"
    else:
        return None, "Error fetching data from Google Maps API"

import math

def haversine(coord1, coord2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Coordinates in decimal degrees
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance


lat = '23.0047206'
lng = '72.558553'
km = 4

min_lat, max_lat, min_lon, max_lon = get_bounds(lat=float(lat), lon=float(lng), radius_km=km)

step_size = 0.001  # Step size in degrees

coordinates = generate_coordinates_within_bounds(min_lat, max_lat, min_lon, max_lon, step_size)

# Print the coordinates
print(len(coordinates))
pdb.set_trace()
distances = []
cords = []

final_coords = []

number = 100

pdb.set_trace()

for i in range(int(len(coordinates)/number)):
    j = i * number
    j = random_number = random.randint(j-number, j)
    destination_lat = coordinates[j][0]
    destination_lng = coordinates[j][1]

    final_coords.append(f'{destination_lat},{destination_lng}')

    print(j)

    if False:
        api_key = "AIzaSyBevStMFDR_VLoRnAeAeJF_OhXARBbLc5k"

        distance, duration = get_distance(lat, lng, destination_lat, destination_lng, api_key)
        print('-------------------------------------------------------------')
        print(destination_lat, destination_lng)
        print(j)
        if distance:
            print(f"Distance: {distance}")
            print(f"Duration: {duration}")
            distances.append(distance)
            cords.append(coordinates)
            # Example usage
            coord1 = (lat, lng)  # Example: New York City (lat, lon)
            coord2 = (destination_lat, destination_lng) # Example: Los Angeles (lat, lon)

            distance = haversine(coord1, coord2)
            print(f"The distance is {distance:.2f} km")

        else:
            print("Error:", duration)

data = []

for dis in distances:
    data.append(float(dis.replace(' km','')))


# max_val, min_val = max(data), min(data)
# less_1_5, more_1_5 = sum(x < 1.5 for x in data), sum(x > 1.5 for x in data)
# less_2_5, more_2_5 = sum(x < 2.5 for x in data), sum(x > 2.5 for x in data)

pdb.set_trace()


# fr = {'less_1_0':less_1_0,'more_1_0':more_1_0,'less_1_5':less_1_5,'more_1_5':more_1_5,'less_2_0':less_2_0,'more_2_0':more_2_0,'less_2_5':less_2_5,'more_2_5':more_2_5}

# {

# 'less_1_0': 15, 
# 'more_1_0': 62, 
# 'less_1_5': 33, 
# 'more_1_5': 42, 
# 'less_2_0': 46, 
# 'more_2_0': 30, 
# 'less_2_5': 54, 
# 'more_2_5': 23

# }
