import re

# Sample JSON-like dictionary you provided earlier
json_mapping = {
  "developerGroupName": "group_name",
  "yearOfEstablishment": "year_of_establishment",
  "projectsDelivered": "no_of_projects_delivered",
  "key_projects": "key_projects",
  "keyProjects": "key_projects",
  "keyPromoters": "key_promoters",
  "contactName": "name",
  "contactNumber": "number",
  "contactEmail": "email",
  "alternateName": "alternate_name",
  "alternateNumber": "alternate_number",
  "alternateEmail": "alternate_email",
  "projectId": "project_id",
  "projectName": "project_name",
  "developedBy": "developed_by",
  "projectLocation": "location_of_project",
  "googlePin": "google_Pin",
  "projectType": "type_of_project",
  "bedrooms": "type_of_apartments",
  "ageOfPropertyDeveloper": "age_of_property_developer",
  "ageOfPropertyRERA": "age_of_property_rera",
  "plotArea": "plot_area",
  "architect": "architect",
  "constructionCompany": "construction_company",
  "numberOfBlocks": "no_of_blocks",
  "numberOfUnits": "no_of_units",
  "numberOfFloors": "no_of_floors",
  "numberOfBasements": "no_of_basements",
  "jodiPossible": "jodi_possible",
  "overallVastu": "NA",
  "entryExitWind": "NA",
  "centralAC": "central_air_conditioning",
  "petFriendly": "pet_friendly",
  "spiritualAttraction": "spiritual_or_religious_attraction",
  "parkingType": "type_of_parking",
  "unitTypes": "unit_configuration",
  "layoutTypes": "unit_type",
  "unitsPerFloor": "no_of_units_per_floor",
  "liftsPerFloor": "no_of_lifts_per_floor",
  "privateLifts": "private_lifts",
  "numberOfPrivateLifts": "no_private_lifts",
  "commonTerrace": "common_terrace_accessible",
  "sizeOfMainBalcony": "size_of_balcony",
  "sizeOfMasterBedroom": "size_of_master_bedroom",
  "sizeOfKitchen": "size_of_kitchen",
  "sizeOfPrivateTerrace": "size_of_private_terrace",
  "sizeOfUnit": "size_of_unit",
  "carpetArea": "carpet_area_rera",
  "numberOfBathrooms": "no_of_attached_bathrooms",
  "servantRoomAvailable": "servant_room_available",
  "pujaRoomAvailable": "separate_puja_room_available",
  "numberOfBalconies": "no_of_balconies",
  "parkingAllotted": "no_of_parking_allotted",
  "perSqFtRate": "per_sqft_rate_saleable",
  "plcOptions_garden": "plc_garden",
  "plcOptions_road_facing": "plc_road_facing",
  "plcOptions_corner": "plc_corner",
  "plcOptions_others": "plc_others",
  "developmentCharges": "development_charges",
  "advanceMaintenance": "advance_maintenance",
  "maintenanceDeposit": "maintenance_deposit",
  "specificExpenses": "other_specific_expenses",
  "saleDeedValue": "sale_deed_value",
  "gstApplicable": "gst_applicable",
  "loanAvailability": "loan_availability",
  "remarks": "remarks"
}

def update_name_attributes(html_file, output_file, json_mapping):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Loop through the json_mapping and replace the name="" attributes
    for old_name, new_name in json_mapping.items():
        # Create a regex pattern to find name="old_name" and replace it with name="new_name"
        pattern = fr'name="{old_name}"'
        replacement = f'name="{new_name}"'
        html_content = re.sub(pattern, replacement, html_content)

    # Write the updated content to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML file processed and saved as {output_file}")

# Example usage
update_name_attributes(r'C:\Users\Divyam Shah\OneDrive\Desktop\Dynamic Labz\Clients\Clients\Square Second Consultancy\SSC\SSC\templates\property_detail_form.html', r'C:\Users\Divyam Shah\OneDrive\Desktop\Dynamic Labz\Clients\Clients\Square Second Consultancy\SSC\SSC\templates\property_detail_form_name_uopdated.html', json_mapping)
