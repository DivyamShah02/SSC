import requests

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
