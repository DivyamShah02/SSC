import os, json, random

def generate_building_details():
    building_details = []
    for i in range(100):
        building_name = f"{random.choice(['Skyline', 'Star', 'Galaxy', 'Urban']) } {random.choice(['Residency', 'Heights', 'Towers', 'Apartments'])}"
        group_name = f"Group {chr(65+i)}"
        building = {}
        bhks = []

        min_bhk = random.randint(2, 6)

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
            "location_of_project": f"{random.randint(100, 999)} {random.choice(['Street', 'Avenue', 'Road'])}",
            "google_pin": "https://maps.app.goo.gl/FxcQVyRjHuTiwx9f6",
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
                "per_sqft_rate_saleable": round(random.uniform(5000.00, 12000.00), 2)
            }
            building['unit_details'].append(temp_dict)
        
        building_details.append(building)
    
    return building_details

building_details = generate_building_details()

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

folder = os.getcwd()
filename = generate_file_name(folder=folder, file_name='data.json')
with open(filename, 'w') as json_file:
    json.dump(building_details, json_file, indent=4)
print(f'Data save to {filename}')