import os
from django.db.models import Q
from .library.Config import Config
from Property.models import BuildingDetails, UnitDetails, Amenities
from Property.serializers import UnitDetailsSerializer, BuildingDetailsSerializer, AmenitiesSerializer
from ClientDetail.models import PropertyInquiry
from ClientDetail.serializers import PropertyInquirySerializer
from SSC.settings import BASE_DIR
from django.shortcuts import get_object_or_404



class Sorter:
    def __init__(self) -> None:
        config_path = os.path.join(BASE_DIR, 'SorterSession', 'sorting_config.ini')
        self.config = Config(filename=config_path)

    def update_client_preferences(self, client_data):
        """
        Updates the client preferences based on defined configuration variations.
        """
        try:
            updated_data = client_data.copy()

            # Carpet area: apply a variation of 15% on both sides of the range
            carpet_area_variation = float(self.config.client_data_variation.carpet_area_variation)
            min_carpet_area = float(client_data.get('min_carpet_area', 0))
            updated_data['min_carpet_area'] = min_carpet_area * (1 + (carpet_area_variation / 100))

            # Budget handling
            min_budget = float(client_data.get('budget_min', 0)) * 10000000
            max_budget = float(client_data.get('budget_max', 0)) * 10000000

            decision_driven = client_data.get('decision_driven_by')
            if decision_driven == 'budget_driven':
                budget_variation = float(self.config.client_data_variation.budget_variation_budget_driven)
                updated_data['budget_min'] = min_budget * (1 + (budget_variation / 100))
                updated_data['budget_max'] = max_budget * (1 + (budget_variation / 100))

            elif decision_driven == 'choice_driven':
                min_variation = float(self.config.client_data_variation.budget_variation_choice_driven_min)
                max_variation = float(self.config.client_data_variation.budget_variation_choice_driven_max)
                updated_data['budget_min'] = min_budget * (1 + (min_variation / 100))
                updated_data['budget_max'] = max_budget * (1 + (max_variation / 100))

            # Timeline: add 15% in the time on the higher side
            if 'time_to_seal_deal' in client_data:
                timeline_variation = float(self.config.client_data_variation.timeline_variation)
                timeline_value = int(client_data.get('time_to_seal_deal', 0))  # Assuming months
                updated_data['time_to_seal_deal'] = int(timeline_value * (1 + (timeline_variation / 100)))

            # Format bedroom data
            bedrooms_list = client_data.get("bedrooms", "").split(', ')
            formatted_bedrooms = [b.replace('_bhk', 'BHK').upper() for b in bedrooms_list]
            updated_data["bedrooms"] = ' | '.join(formatted_bedrooms)

            return updated_data

        except (KeyError, ValueError, TypeError) as e:
            # Log error and raise appropriate exception
            print(f"Error updating client preferences: {e}")
            raise ValueError(f"Invalid data format: {str(e)}")

    def get_pre_validated_property(self, updated_client_data):
        """
        Returns properties that match the client's updated preferences.
        """
        try:
            bedrooms = updated_client_data.get('bedrooms', '').split(' | ')
            min_carpet_area = updated_client_data.get('min_carpet_area', 0)
            budget_min = updated_client_data.get('budget_min', 0)
            budget_max = updated_client_data.get('budget_max', 0)
            unit_type = 'simplex'

            validated_property = []
            for bedroom in bedrooms:
                property_unit_matched = UnitDetails.objects.filter(unit_configuration__icontains=bedroom, size_of_unit__gte=min_carpet_area, unit_type__icontains=unit_type)  # Assuming unit_type as 'Simplex'

                if len(property_unit_matched) !=0:
                    for property in property_unit_matched:
                        unit_price = property.size_of_unit * property.per_sqft_rate_saleable
                        if budget_min <= unit_price and budget_max >= unit_price:
                            validated_property.append(property.id)

            return validated_property

        except Exception as e:
            print(f"Error fetching pre-validated properties: {e}")
            raise ValueError(f"Error in property validation: {str(e)}")

    def generate_property_list(self, updated_client_data, validated_properties):
        scored_units = []
        for property in validated_properties:
            scored_properties = self.calculate_property_score(client_preferences=updated_client_data, unit_id=property)
            scored_units.append(scored_properties)

        sorted_data = sorted(scored_units, key=lambda x: x['score'], reverse=True)
        return sorted_data



    def calculate_property_score(self, client_preferences, unit_id):
        score = 0

        unit_data_obg = get_object_or_404(UnitDetails, id=unit_id)
        unit_data = UnitDetailsSerializer(unit_data_obg).data

        property_data_obj = get_object_or_404(BuildingDetails, building_id=unit_data_obg.building_id)
        property_data = BuildingDetailsSerializer(property_data_obj).data

        amenties_data_obj = get_object_or_404(Amenities, building_id=unit_data_obg.building_id)
        amenties_data = AmenitiesSerializer(amenties_data_obj).data

        # 1. Attached Washrooms
        client_washrooms = int(client_preferences.get('attached_washrooms', 0))
        property_washrooms = int(unit_data.get('no_of_attached_bathrooms', 0))
        if property_washrooms == client_washrooms:
            score += int(self.config.scoring.attached_washroom_exact)
        elif property_washrooms > client_washrooms:
            score += int(self.config.scoring.attached_washroom_more)
        else:
            score += int(self.config.scoring.attached_washroom_less)

        # 2. Floor Preference
        client_floor_preference_lst = str(client_preferences.get('floor_preference', '')).split('-')
        if len(client_floor_preference_lst) == 2:
            property_total_floors = int(property_data.get('no_of_floors', 0))
            if property_total_floors >= int(client_floor_preference_lst[0]) and property_total_floors <= int(client_floor_preference_lst[1]):
                score += int(self.config.scoring.floor_preference_exact)
            else:
                score += int(self.config.scoring.floor_preference_other)

        # 3. Servant Room
        if unit_data.get('servant_room_available'):
            score += int(self.config.scoring.servant_room)

        # 4. Type of Society
        # client_society_type = client_preferences.get('society_type', '')
        # property_society_type = unit_data.get('society_type', '')
        # if client_society_type == property_society_type:
        #     score += int(self.config.scoring.society_type_exact)
        # else:
        #     score += int(self.config.scoring.society_type_other)

        # 5. Flat Preference on 1 Floor
        client_flat_preference_lst = str(client_preferences.get('flats_per_floor', '')).split('-')
        if len(client_flat_preference_lst) == 2:
            property_units_per_floor = int(property_data.get('no_of_units_per_floor', 0))
            if property_units_per_floor >= int(client_flat_preference_lst[0]) and property_units_per_floor <= int(client_flat_preference_lst[1]):
                score += int(self.config.scoring.flat_preference_exact)
            else:
                score += int(self.config.scoring.flat_preference_less)

        # 6. Religious Place
        if client_preferences.get('religious_preference') in str(property_data.get('spiritual_or_religious_attraction')):
            score += int(self.config.scoring.religious_place_match)
        else:
            score += int(self.config.scoring.religious_place_no_match)

        # 7. Private Elevator
        if unit_data.get('private_lifts'):
            score += int(self.config.scoring.private_elevator_exists)
        else:
            score += int(self.config.scoring.private_elevator_no)

        # 8. Central AC
        client_ac = client_preferences.get('central_air_conditioning', 'Maybe')
        property_ac = property_data.get('central_air_conditioning', False)
        if client_ac == 'Yes' and property_ac:
            score += int(self.config.scoring.central_ac_match_yes_yes)
        elif client_ac == 'No' and not property_ac:
            score += int(self.config.scoring.central_ac_match_no_no)
        else:
            score += int(self.config.scoring.central_ac_other)

        # 9. Parking
        client_parking = int(client_preferences.get('min_parking_slots', 0))
        property_parking = int(unit_data.get('no_of_parking_allotted', 0))
        if property_parking >= client_parking:
            score += int(self.config.scoring.parking_exact_or_more)
        elif property_parking == client_parking - 1:
            score += int(self.config.scoring.parking_one_less)
        else:
            score += int(self.config.scoring.parking_two_or_more_less)

        # 10. Stack Parking
        client_stack_parking = client_preferences.get('stack_parking', 'Maybe')
        property_stack_parking = property_data.get('type_of_parking', 'No')
        if client_stack_parking == property_stack_parking:
            score += int(self.config.scoring.stack_parking_exact)
        else:
            score += int(self.config.scoring.stack_parking_other)

        # 11. Amenities
        client_amenities = set(client_preferences.get('amenities', '').split(', '))
        for amenities in client_amenities:
            if amenties_data.get(amenities, False):
                score += int(self.config.scoring.amenities_per_match)

        return {'unit_id':unit_id, 'score':score}

if __name__ == '__main__':
    inquiry_id = 2
    client_data = get_object_or_404(PropertyInquiry, id=inquiry_id)

    serializer = PropertyInquirySerializer(client_data)

    sorter = Sorter()

    # Update client preferences and get validated properties
    updated_client_data = sorter.update_client_preferences(client_data=serializer.data)
    validated_properties = sorter.get_pre_validated_property(updated_client_data=updated_client_data)

    if not validated_properties:
        exit()

    # Prepare the response data
    property_list = validated_properties

    scored_properties = sorter.calculate_property_score(client_preferences=updated_client_data, unit_id=validated_properties[0])

