from django.shortcuts import render
from django.http import HttpResponse
from Property.models import BuildingDetails, UnitDetails, Amenities
import random
import json
from .cords import final_cords
import requests
import os

def temp_data(request):
    data = generate_building_details(number_of_entries=1000)
    folder = r'C:\Users\Divyam Shah\OneDrive\Desktop\Dynamic Labz\Clients\Square Second Consultancy\SSC\SSC\Misc\data'
    filename = generate_file_name(folder=folder, file_name='data.json')
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f'Data save to {filename}')
    
    for building in data:
        new_building = BuildingDetails(
            building_id = building['building_details']["building_id"],
            group_name = building['building_details']["group_name"],
            head_image = "head.jpg",
            sec_image_1 = "sec_1.jpg",
            sec_image_2 = "sec_2.jpg",
            year_of_establishment = building['building_details']["year_of_establishment"],
            no_of_projects_delivered = building['building_details']["no_of_projects_delivered"],
            key_projects = building['building_details']["key_projects"],
            key_promoters = building['building_details']["key_promoters"],
            name = building['building_details']["name"],
            number = building['building_details']["number"],
            alternate_name = building['building_details']["alternate_name"],
            alternate_number = building['building_details']["alternate_number"],
            project_id = building['building_details']["project_id"],
            project_name = building['building_details']["project_name"],
            developed_by = building['building_details']["developed_by"],
            location_of_project = building['building_details']["location_of_project"],
            google_pin_lat = building['building_details']["google_pin_lat"],
            google_pin_lng = building['building_details']["google_pin_lng"],
            type_of_project = building['building_details']["type_of_project"],
            type_of_apartments = building['building_details']["type_of_apartments"],
            age_of_property_developer = building['building_details']["age_of_property_developer"],
            age_of_property_rera = building['building_details']["age_of_property_rera"],
            plot_area = building['building_details']["plot_area"],
            architect = building['building_details']["architect"],
            construction_company = building['building_details']["construction_company"],
            no_of_blocks = building['building_details']["no_of_blocks"],
            no_of_units = building['building_details']["no_of_units"],
            no_of_floors = building['building_details']["no_of_floors"],
            no_of_basements = building['building_details']["no_of_basements"],
            central_air_conditioning = building['building_details']["central_air_conditioning"],
            pet_friendly = building['building_details']["pet_friendly"],
            spiritual_or_religious_attraction = building['building_details']["spiritual_or_religious_attraction"],
            type_of_parking = building['building_details']["type_of_parking"],
            plc = building['building_details']["plc"],
            floor_rise = building['building_details']["floor_rise"],
            development_charges = building['building_details']["development_charges"],
            advance_maintenance = building['building_details']["advance_maintenance"],
            maintenance_deposit = building['building_details']["maintenance_deposit"],
            other_specific_expenses = building['building_details']["other_specific_expenses"],
            sale_deed_value_min = building['building_details']["sale_deed_value_min"],
            sale_deed_value_max = building['building_details']["sale_deed_value_max"],
            gst_applicable = building['building_details']["gst_applicable"],
            loan_availability = building['building_details']["loan_availability"],
            remarks = building['building_details']["remarks"]
        ) 
        new_building.save()

        for unit in building['unit_details']:
            new_unit = UnitDetails(
                building_id = unit["building_id"],
                unit_configuration = unit["unit_configuration"],
                unit_type = unit["unit_type"],
                no_of_units_per_floor = unit["no_of_units_per_floor"],
                no_of_lifts_per_floor = unit["no_of_lifts_per_floor"],
                private_lifts = unit["private_lifts"],
                common_terrace_accessible = unit["common_terrace_accessible"],
                size_of_private_terrace = unit["size_of_private_terrace"],
                size_of_unit = unit["size_of_unit"],
                carpet_area_rera = unit["carpet_area_rera"],
                jodi_possible = unit["jodi_possible"],
                no_of_attached_bathrooms = unit["no_of_attached_bathrooms"],
                servant_room_available = unit["servant_room_available"],
                separate_puja_room_available = unit["separate_puja_room_available"],
                no_of_balconies = unit["no_of_balconies"],
                no_of_parking_allotted = unit["no_of_parking_allotted"],
                per_sqft_rate_saleable = unit["per_sqft_rate_saleable"],
                google_pin_lat = building['building_details']["google_pin_lat"],
                google_pin_lng = building['building_details']["google_pin_lng"],
            )
            new_unit.save()

        ammenties = Amenities(
            building_id = building['amenities']["building_id"],
            swimming_pool = building['amenities']["swimming_pool"],
            gym_fitness_center = building['amenities']["gym_fitness_center"],
            clubhouse = building['amenities']["clubhouse"],
            children_play_area = building['amenities']["children_play_area"],
            sports_facilities = building['amenities']["sports_facilities"],
            jogging_walking_tracks = building['amenities']["jogging_walking_tracks"],
            common_gardens = building['amenities']["common_gardens"],
            community_hall = building['amenities']["community_hall"],
            security_24_7 = building['amenities']["security_24_7"],
            cctv_surveillance = building['amenities']["cctv_surveillance"],
            power_backup = building['amenities']["power_backup"],
            waste_management = building['amenities']["waste_management"],
            concierge = building['amenities']["concierge"],
            reading_room = building['amenities']["reading_room"],
            home_theatre = building['amenities']["home_theatre"],
            internet_connectivity = building['amenities']["internet_connectivity"],
            guest_rooms = building['amenities']["guest_rooms"],
            pet_friendly_areas = building['amenities']["pet_friendly_areas"],
            spa_salon = building['amenities']["spa_salon"],
            co_working_space = building['amenities']["co_working_space"],
            terrace_amenities = building['amenities']["terrace_amenities"],
        )
        ammenties.save()

    return HttpResponse('Data uploaded')


def generate_building_details(number_of_entries):
    building_details = []
    
    for i in range(number_of_entries):
        # i=i+101
        building_name = f"{random.choice(['Skyline', 'Star', 'Galaxy', 'Urban']) } {random.choice(['Residency', 'Heights', 'Towers', 'Apartments'])}"
        group_name = f"Group {chr(65+i)}"
        building = {}
        bhks = []

        min_bhk = random.randint(2, 6)
        
        coords= final_cords[i].split(',')
        google_pin_lat = str(coords[0]).strip()
        google_pin_lng = str(coords[1]).strip()
        api_key = 'AIzaSyBevStMFDR_VLoRnAeAeJF_OhXARBbLc5k'  # Replace with your API key
        address = get_address_from_coordinates(google_pin_lat, google_pin_lng, api_key)
        print(address)


        while True:
            max_bhk = random.randint(2, 6)
            if max_bhk >= min_bhk:
                break
        
        for j in range(7):
            if j >= min_bhk and j <= max_bhk:
                bhks.append(f'{j}BHK')


        # for i in range(3):
        #     bhk = random.randint(2, 6)
        #     if bhk not in bhks:
        #         bhks.append(str(bhk))
        
        type_of_apartments = ' | '.join(bhks)

        building['building_details'] = {
            "building_id": f"BD{i+1:03}",
            "group_name": group_name,  # Group names A-J
            "year_of_establishment": random.randint(1980, 2024),
            "no_of_projects_delivered": random.randint(5, 20),
            "key_projects": f", ".join([f"Project {j+1}" for j in range(random.randint(2, 5))]),
            "key_promoters": f", ".join([f"{random.choice(['Mr.', 'Ms.'])} {random.randint(100, 999)} {random.choice(['Smith', 'Johnson', 'Lee', 'Garcia'])}" for _ in range(2)]),
            "name": building_name,
            "number": f"{random.randint(1000000000, 9999999999)}",
            "alternate_name": random.choice([None, f"{random.choice(['Metro', 'Prime', 'Elite'])} {building_name}"][:50]),  # Limit length to 50 characters
            "alternate_number": random.choice([None, f"{random.randint(1000000000, 9999999999)}"]),
            "project_id": f"PRJ{i+1:03}",
            "project_name": building_name,
            "developed_by": group_name,
            "location_of_project": address,
            "google_pin_lat": google_pin_lat,
            "google_pin_lng": google_pin_lng,
            "type_of_project": "Residential",
            "type_of_apartments": type_of_apartments,  # 1-4 BHK options
            # "type_of_apartments": f"{random.randint(1, 4)}BHK",  # 1-4 BHK options
            "age_of_property_developer": random.randint(10, 50),
            "age_of_property_rera": random.randint(5, 20),
            "plot_area": f"{random.randint(10000, 50000)} sq ft",
            "architect": f"{random.choice(['Ar. ', 'M/s. '])}{random.randint(100, 999)} {random.choice(['Architects', 'Associates'])}",
            "construction_company": f"{random.choice(['BuildCorp', 'ConstTech', 'SturdyHomes'])}",
            "no_of_blocks": random.randint(2, 10),
            "no_of_units": random.randint(50, 200),
            "no_of_floors": random.randint(10, 30),
            "no_of_basements": random.randint(0, 2),
            "central_air_conditioning": random.choice([True, False]),
            "pet_friendly": random.choice([True, False]),
            "spiritual_or_religious_attraction": random.choice([None, "Temple within complex", "Mosque nearby", "Church in vicinity"]),
            "type_of_parking": random.choice(["Covered", "Open", "Stilted"]),
            "plc": round(random.uniform(150.00, 500.00), 2),  # Random PLC between 150 and 500
            "floor_rise": round(random.uniform(30.00, 80.00), 2),  # Random floor rise between 30 and 80
            "development_charges": round(random.uniform(1000.00, 3000.00), 2),
            "advance_maintenance": round(random.uniform(15000.00, 30000.00), 2),
            "maintenance_deposit": round(random.uniform(30000.00, 60000.00), 2),
            "other_specific_expenses": random.choice([None, "N/A", "Electricity charges", "Water charges", "Garbage collection"]),
            "sale_deed_value_min": round(random.uniform(3000000.00, 7000000.00), 2),
            "sale_deed_value_max": round(random.uniform(5000000.00, 10000000.00), 2),
            "gst_applicable": round(random.uniform(3.00, 7.00), 2),
            "loan_availability": random.choice([True, False]),
            "remarks": random.choice([None, "Well-connected with metro and bus services", "Near schools and hospitals", "Close to shopping malls", "Peaceful neighborhood"])
        }
        building['amenities'] = {
            "building_id": building['building_details']["building_id"],
            "swimming_pool": random.choice([True, False]),
            "gym_fitness_center": random.choice([True, False]),
            "clubhouse": random.choice([True, False]),
            "children_play_area": random.choice([True, False]),
            "sports_facilities": random.choice([True, False]),
            "jogging_walking_tracks": random.choice([True, False]),
            "common_gardens": random.choice([True, False]),
            "community_hall": random.choice([True, False]),
            "security_24_7": random.choice([True, False]),
            "cctv_surveillance": random.choice([True, False]),
            "power_backup": random.choice([True, False]),
            "waste_management": random.choice([True, False]),
            "concierge": random.choice([True, False]),
            "reading_room": random.choice([True, False]),
            "home_theatre": random.choice([True, False]),
            "internet_connectivity": random.choice([True, False]),
            "guest_rooms": random.choice([True, False]),
            "pet_friendly_areas": random.choice([True, False]),
            "spa_salon": random.choice([True, False]),
            "co_working_space": random.choice([True, False]),
            "terrace_amenities": random.choice([True, False])
        }
        
        building['unit_details'] = []
        unit_number = random.randint(1, 6)
        for i in range(unit_number):    
            temp_dict = {
                "building_id": building['building_details']["building_id"],
                "unit_configuration": f"{random.randint(min_bhk, max_bhk)}BHK",
                "unit_type": random.choice(["Simplex", "Duplex", "Pent House"]),
                "no_of_units_per_floor": random.randint(2, 6),
                "no_of_lifts_per_floor": random.randint(1, 3),
                "private_lifts": random.choice([True, False]),
                "common_terrace_accessible": random.choice([True, False]),
                "size_of_private_terrace": round(random.uniform(100.00, 300.00), 2) if random.choice([True, False]) else None,
                "size_of_unit": round(random.uniform(800.00, 1500.00), 2),
                "carpet_area_rera": round(random.uniform(600.00, 1200.00), 2),
                "jodi_possible": random.choice([True, False]),
                "no_of_attached_bathrooms": random.randint(1, 3),
                "servant_room_available": random.choice([True, False]),
                "separate_puja_room_available": random.choice([True, False]),
                "no_of_balconies": random.randint(1, 3),
                "no_of_parking_allotted": random.randint(0, 2),
                "per_sqft_rate_saleable": round(random.uniform(5000.00, 12000.00), 2),
                "google_pin_lat": google_pin_lat,
                "google_pin_lng": google_pin_lng,
                "location_of_project": address,

            }
            building['unit_details'].append(temp_dict)
        
        building_details.append(building)
    
    return building_details


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

def generate_file_name(folder, file_name):
    """Generate unique file name to avoid conflicts."""
    process_file_path = os.path.join(folder, file_name)
    counter = 1
    while os.path.exists(process_file_path):
        base_name, ext = os.path.splitext(file_name)
        base_name = str(base_name).replace(f'_{counter-1}','')
        process_file_path = os.path.join(folder, f"{base_name}_{counter}{ext}")
        counter += 1
    return process_file_path

