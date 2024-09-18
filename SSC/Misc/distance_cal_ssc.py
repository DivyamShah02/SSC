import requests

def get_address_from_coordinates(lat, lng, api_key):
    # Geocoding endpoint
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {  
    'latlng': f'{lat},{lng}',
    'key':api_key
    }
    
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the API returned any results
        if data['results']:
            # Extract the formatted address
            address = data['results'][0]['formatted_address']
            return address
        else:
            return "No address found for the provided coordinates."
    else:
        return f"Error: {response.status_code}"

# Example usage
api_key = 'AIzaSyBevStMFDR_VLoRnAeAeJF_OhXARBbLc5k'  # Replace with your API key
lat = '23.0047206'
lng = '72.558553'
latitude = '23.0047206'
longitude = '72.558553'


address = get_address_from_coordinates(latitude, longitude, api_key)
print(address)
