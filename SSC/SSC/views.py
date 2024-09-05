from django.shortcuts import render
from django.http import HttpResponse
from Property.models import BuildingDetails, UnitDetails, Amenities
import json

def temp_datat(request):
    json_file = r'C:\Users\Divyam Shah\OneDrive\Desktop\Dynamic Labz\Clients\Square Second Consultancy\SSC\SSC\Misc\data_2.json'
    with open(json_file, 'r') as file:
        # Parse JSON content and convert it to a dictionary
        data = json.load(file)

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
            google_pin = building['building_details']["google_pin"],
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


def temp_data(request):
    search_string = '3BHK'  # You can replace this with the string you're searching for
    min_carpet_area = '1300'
    budget_min = 1000000
    budget_max = 16000000
    unit_type = 'Simplex'
    matching_properties = BuildingDetails.objects.filter(type_of_apartments__icontains=search_string)
    for match_ in matching_properties:
        property_unit_matched = UnitDetails.objects.filter(building_id=match_.building_id, unit_configuration__icontains=search_string, size_of_unit__gte=min_carpet_area, unit_type__icontains=unit_type)
        if len(property_unit_matched) !=0:
            for property in property_unit_matched:
                unit_price = property.size_of_unit * property.per_sqft_rate_saleable
                if budget_min <= unit_price and budget_max >= unit_price:
                    print(f'Property - {match_.building_id}')
                    print(property.id)
                    print(unit_price)
                    print(f'bathroom - {property.no_of_attached_bathrooms}')
                    print('----------------------------')
                
    return HttpResponse('Data uploaded')
