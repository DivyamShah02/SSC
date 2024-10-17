import requests

def get_distance(origin_lat, origin_lng, destination_lat, destination_lng):
    
    api_key = "AIzaSyAcRWpebJJ-1GyUv8NkMPVizMtqLWBHotk"

    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": f"{origin_lat},{origin_lng}",
        "destinations": f"{destination_lat},{destination_lng}",
        "key": api_key,
        "mode": "driving"  # change this to "walking", "bicycling", "transit" if needed
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['rows'][0]['elements'][0]['status'] == 'OK':
            distance = data['rows'][0]['elements'][0]['distance']['text']
            duration = data['rows'][0]['elements'][0]['duration']['text']
            return distance, duration
        else:
            return None, "No route found"
    else:
        return None, "Error fetching data from Google Maps API"


def get_address(lat, lng):
    
    api_key = "AIzaSyAcRWpebJJ-1GyUv8NkMPVizMtqLWBHotk"
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        'latlng': f'{lat},{lng}',
        'key': api_key
    }
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        result = response.json()
        if result['results']:
            return result['results'][0]['formatted_address']
        else:
            return "Address not found"
    else:
        return "Error fetching data from Google Maps API"
