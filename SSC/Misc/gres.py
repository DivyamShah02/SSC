from datetime import datetime

def calculate_points(property_age, age_of_property_by_developer):
    try:
        # Parse the building_detail into a month and year
        building_month, building_year = map(int, age_of_property_by_developer.split('-'))
        building_date = datetime(year=building_year, month=building_month, day=1)
        
        # Get the current date for comparison
        current_date = datetime.now()
        
        # Calculate the difference in months between the current date and the building date
        months_difference = (building_date.year - current_date.year) * 12 + (building_date.month - current_date.month)

        # Define the ranges for client details
        client_ranges = {
            "0 to 12 months old": (-12, 0),
            "12 to 36 months old": (-36, -12),
            "36 to 48 months": (-48, -36),
            "Upcoming 6 - 12 months": (6, 12),
            "Upcoming 12 to 36 months": (12, 36),
            "Flexible": None
        }
        
        # Handle the 'Flexible' case
        if property_age == "Flexible":
            return 10

        # Check if the building's date fits the client's range
        client_min, client_max = client_ranges[property_age]
        
        if client_min <= months_difference <= client_max:
            return 10  # Direct match
        else:
            # Handle concurrent options, skipping 'Flexible'
            for range_name, range_values in client_ranges.items():
                if range_name == "Flexible":
                    continue  # Skip the 'Flexible' option
                range_min, range_max = range_values
                if range_name != property_age and range_min <= months_difference <= range_max:
                    return 5  # Concurrent match

        return 0  # No match
    except:
        return 0
# Example usage:
property_age = "Flexible"
age_of_property_by_developer = "11-2025"
points = calculate_points(property_age, age_of_property_by_developer)
print(f"Points awarded: {points}")