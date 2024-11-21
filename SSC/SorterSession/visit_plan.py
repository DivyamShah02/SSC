import googlemaps
from datetime import datetime, timedelta

def create_visit_plan(starting_point, properties, start_date_time):
    """
    Create a visit plan for properties based on proximity and duration at each property.
    
    :param api_key: Google Maps API key
    :param starting_point: Tuple of (latitude, longitude) for the starting location
    :param properties: List of dicts [{'id': 4, 'coords': (lat, lon)}, ...]
    :param start_date_time: Starting datetime object
    :return: A list of visit plans with time and locations
    """

    gmaps = googlemaps.Client(key='AIzaSyAcRWpebJJ-1GyUv8NkMPVizMtqLWBHotk')
    current_location = starting_point
    current_time = start_date_time
    visit_plan = []

    while properties:
        # Get distances to all properties
        distances = []
        for property in properties:
            result = gmaps.distance_matrix(
                origins=[current_location],
                destinations=[property['coords']],
                mode="driving"
            )
            travel_time = result['rows'][0]['elements'][0]['duration']['value']  # Travel time in seconds
            distances.append((property, travel_time))

        # Find the nearest property
        nearest_property, travel_time = min(distances, key=lambda x: x[1])
        
        # Update visit plan
        arrival_time = current_time + timedelta(seconds=travel_time)
        departure_time = arrival_time + timedelta(hours=1)
        visit_plan.append({
            "property_id": nearest_property['id'],  # Include property ID
            "coords": nearest_property['coords'],  # Include property coordinates
            "arrival_date": arrival_time.strftime("%Y-%m-%d"),
            "arrival_time": arrival_time.strftime("%H:%M"),
            "departure_time": departure_time.strftime("%I:%M %p on %d/%m/%Y")
        })

        # Update current location, time, and remove visited property
        current_location = nearest_property['coords']
        current_time = departure_time
        properties.remove(nearest_property)

    return visit_plan


# Example usage
if __name__ == "__main__":
    starting_point = (23.0225, 72.5714)  # Example starting point (Ahmedabad)
    properties = [
        (23.0300, 72.5800), (23.0150, 72.5600), (23.0400, 72.5900)
    ]  # Example properties
    start_date_time = datetime(2024, 11, 20, 22, 0)  # Starting at 10 PM

    plan = create_visit_plan(starting_point, properties, start_date_time)
    for step in plan:
        print(f"Visit {step['property']}:\n"
              f"  Arrival: {step['arrival_time']}\n"
              f"  Departure: {step['departure_time']}\n")
