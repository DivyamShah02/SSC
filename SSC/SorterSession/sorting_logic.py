import os
from .library.Config import Config
from .library.DistanceCalculator import get_distance
from Property.models import BuildingDetails, UnitDetails, Amenities
from Property.serializers import UnitDetailsSerializer, BuildingDetailsSerializer, AmenitiesSerializer
from ClientDetail.models import PropertyInquiry
from ClientDetail.serializers import PropertyInquirySerializer
from SSC.settings import BASE_DIR
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
import math
import pdb
from datetime import datetime


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
            if 'budget' in str(decision_driven).lower():
                budget_variation = float(self.config.client_data_variation.budget_variation_budget_driven)
                updated_data['budget_min'] = min_budget * (1 + (budget_variation / 100))
                updated_data['budget_max'] = max_budget * (1 + (budget_variation / 100))

            elif 'choice' in str(decision_driven).lower():
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
            formatted_bedrooms = [b.replace('_bhk', ' BHK').upper() for b in bedrooms_list]
            updated_data["bedrooms"] = ' | '.join(formatted_bedrooms)

            return updated_data

        except (KeyError, ValueError, TypeError) as e:
            # Log error and raise appropriate exception
            print(f"Error updating client preferences: {e}")
            raise ValueError(f"Invalid data format: {str(e)}")

    def get_bounds(self, lat, lon, radius_km):
        """
        Get the bounding box for a given point and radius.
        """
        R = 6371  # Earth radius in kilometers

        # Calculate the bounding box
        lat_radians = math.radians(lat)
        lon_radians = math.radians(lon)
        radius_degrees = radius_km / R * (180 / math.pi)

        min_lat = lat - radius_degrees
        max_lat = lat + radius_degrees

        min_lon = lon - radius_degrees / math.cos(lat_radians)
        max_lon = lon + radius_degrees / math.cos(lat_radians)

        return min_lat, max_lat, min_lon, max_lon

    def get_pre_validated_property(self, updated_client_data):
        """
        Returns properties that match the client's updated preferences.
        """
        try:
            bedrooms = updated_client_data.get('bedrooms', '').split(' | ')
            min_carpet_area = updated_client_data.get('min_carpet_area', 0)
            budget_min = updated_client_data.get('budget_min', 0)
            budget_max = updated_client_data.get('budget_max', 0)

            coords = str(updated_client_data.get('preferred_locations')).split(',')
            unit_types = str(updated_client_data.get('unit_type')).split(',')
            validated_property = []

            for coord in coords:
                lat = float(str(str(coord).strip().split('|')[0]).strip())
                lng = float(str(str(coord).strip().split('|')[1]).strip())
                km = 1.5

                # unit_type = 'Simplex'

                min_lat, max_lat, min_lon, max_lon = self.get_bounds(lat=lat, lon=lng, radius_km=km)

                for bedroom in bedrooms:
                    for unit_type in unit_types:
                        print(bedroom)
                        property_unit_matched = UnitDetails.objects.filter(
                            google_pin_lat__gte=min_lat,
                            google_pin_lng__gte=min_lon,
                            google_pin_lat__lte=max_lat,
                            google_pin_lng__lte=max_lon,
                            unit_configuration__icontains=bedroom, size_of_unit__gte=min_carpet_area, unit_type__icontains=unit_type,
                            base_price__gte=budget_min,
                            base_price__lte=budget_max,
                            active=True
                            )
                        print(len(property_unit_matched))
                        # for pr in property_unit_matched:
                        #     print(pr.id)
                        for property in property_unit_matched:
                            if property.id not in validated_property:
                                validated_property.append(property.id)

            return validated_property

        except Exception as e:
            print(f"Error fetching pre-validated properties: {e}")
            raise ValueError(f"Error in property validation: {str(e)}")

    def generate_property_list(self, updated_client_data, validated_properties):
        scored_units = []
        for property in validated_properties:
            try:
                scored_properties = self.calculate_property_score(
                    client_preferences=updated_client_data, unit_id=property
                )
                scored_units.append(scored_properties)
            except Exception as e:
                # Log the exception and continue with next property
                print(f"Error scoring property {property}: {str(e)}")
        
        sorted_data = sorted(scored_units, key=lambda x: x['score'], reverse=True)
        return sorted_data

    def calculate_property_score(self, client_preferences, unit_id):
        score = 0

        try:
            unit_data_obg = UnitDetails.objects.get(id=unit_id)
        except ObjectDoesNotExist:
            raise NotFound(f"Unit with id {unit_id} not found.")
        
        unit_data = UnitDetailsSerializer(unit_data_obg).data
        
        try:
            property_data_obj = BuildingDetails.objects.get(building_id=unit_data_obg.building_id)
        except ObjectDoesNotExist:
            raise NotFound(f"Building with id {unit_data_obg.building_id} not found.")
        
        property_data = BuildingDetailsSerializer(property_data_obj).data

        try:
            amenities_data_obj = Amenities.objects.get(building_id=unit_data_obg.building_id)
        except ObjectDoesNotExist:
            amenities_data = {}
        else:
            amenities_data = AmenitiesSerializer(amenities_data_obj).data

        score += self._score_attached_washrooms(client_preferences, unit_data)
        score += self._score_floor_preference(client_preferences, property_data)
        score += self._score_servant_room(unit_data)
        score += self._score_flat_preference(client_preferences, property_data)
        score += self._score_religious_place(client_preferences, property_data)
        score += self._score_private_elevator(unit_data)
        score += self._score_central_ac(client_preferences, property_data)
        score += self._score_parking(client_preferences, unit_data)
        score += self._score_stack_parking(client_preferences, property_data)
        score += self._score_amenities(client_preferences, amenities_data)
        score += self._score_age_of_property(client_preferences, property_data)

        return {'unit_id': unit_id, 'score': score}

    def _score_attached_washrooms(self, client_preferences, unit_data):
        client_washrooms = int(client_preferences.get('attached_washrooms', 0))
        property_washrooms = int(unit_data.get('no_of_attached_bathrooms', 0))
        
        if property_washrooms == client_washrooms:
            return int(self.config.scoring.attached_washroom_exact)
        elif property_washrooms > client_washrooms:
            return int(self.config.scoring.attached_washroom_more)
        else:
            return int(self.config.scoring.attached_washroom_less)

    def _score_floor_preference(self, client_preferences, property_data):
        client_floor_range = client_preferences.get('floor_preference', '').split('-')
        property_total_floors = int(property_data.get('no_of_floors', 0))
        
        if len(client_floor_range) == 2:
            if property_total_floors >= int(client_floor_range[0]) and property_total_floors <= int(client_floor_range[1]):
                return int(self.config.scoring.floor_preference_exact)
            else:
                return int(self.config.scoring.floor_preference_other)
        return 0

    def _score_servant_room(self, unit_data):
        return int(self.config.scoring.servant_room) if unit_data.get('servant_room_available') else 0

    def _score_society_preference(self, client_preferences, unit_data):
        client_society_type = client_preferences.get('society_type', '')
        property_society_type = unit_data.get('society_type', '')
        if client_society_type == property_society_type:
            return int(self.config.scoring.society_type_exact)
        else:
            return int(self.config.scoring.society_type_other)

    def _score_flat_preference(self, client_preferences, property_data):
        client_flat_range = client_preferences.get('flats_per_floor', '').split('-')
        property_units_per_floor = int(property_data.get('no_of_units_per_floor', 0))
        
        if len(client_flat_range) == 2:
            if property_units_per_floor >= int(client_flat_range[0]) and property_units_per_floor <= int(client_flat_range[1]):
                return int(self.config.scoring.flat_preference_exact)
            return int(self.config.scoring.flat_preference_less)
        # TODO more floors
        return 0

    def _score_religious_place(self, client_preferences, property_data):
        if property_data.get('spiritual_or_religious_attraction'):
            return int(self.config.scoring.religious_place_match) if client_preferences.get('religious_preference') in property_data.get('spiritual_or_religious_attraction', '') else 0
        else:
            return 0

    def _score_private_elevator(self, unit_data):
        return int(self.config.scoring.private_elevator_exists) if unit_data.get('private_lifts') else int(self.config.scoring.private_elevator_no)

    def _score_central_ac(self, client_preferences, property_data):
        client_ac = client_preferences.get('central_air_conditioning', 'Maybe')
        property_ac = property_data.get('central_air_conditioning', False)

        if client_ac == 'Yes' and property_ac:
            return int(self.config.scoring.central_ac_match_yes_yes)
        elif client_ac == 'No' and not property_ac:
            return int(self.config.scoring.central_ac_match_no_no)
        else:
            return int(self.config.scoring.central_ac_other)

    def _score_parking(self, client_preferences, unit_data):
        client_parking = int(client_preferences.get('min_parking_slots', 0))
        property_parking = int(unit_data.get('no_of_parking_allotted', 0))
        
        if property_parking >= client_parking:
            return int(self.config.scoring.parking_exact_or_more)
        elif property_parking == client_parking - 1:
            return int(self.config.scoring.parking_one_less)
        return int(self.config.scoring.parking_two_or_more_less)

    def _score_stack_parking(self, client_preferences, property_data):
        client_stack_parking = client_preferences.get('stack_parking', 'Maybe')
        property_stack_parking = property_data.get('type_of_parking', 'No')
        
        if client_stack_parking == property_stack_parking:
            return int(self.config.scoring.stack_parking_exact)
        return int(self.config.scoring.stack_parking_other)

    def _score_amenities(self, client_preferences, amenities_data):
        client_amenities = set(client_preferences.get('amenities', '').split(', '))
        score = 0
        for amenity in client_amenities:
            if amenities_data.get(amenity, False):
                score += int(self.config.scoring.amenities_per_match)
        return score
    
    def _score_age_of_property(self, client_preferences, property_data):
        try:
            property_age = client_preferences.get('property_age', '')
            age_of_property_by_developer = property_data.get('age_of_property_by_developer', '')
            building_month, building_year = map(int, age_of_property_by_developer.split('-'))
            building_date = datetime(year=building_year, month=building_month, day=1)
            
            current_date = datetime.now()
            
            months_difference = (building_date.year - current_date.year) * 12 + (building_date.month - current_date.month)

            client_ranges = {
                "0 to 12 months old": (-12, 0),
                "12 to 36 months old": (-36, -12),
                "36 to 48 months": (-48, -36),
                "Upcoming 6 - 12 months": (6, 12),
                "Upcoming 12 to 36 months": (12, 36),
                "Flexible": None
            }
            
            if property_age == "Flexible":
                return 10

            client_min, client_max = client_ranges[property_age]
            
            if client_min <= months_difference <= client_max:
                return 10  # Direct match
            else:
                for range_name, range_values in client_ranges.items():
                    if range_name == "Flexible":
                        continue
                    range_min, range_max = range_values
                    if range_name != property_age and range_min <= months_difference <= range_max:
                        return 5  # Concurrent match

            return 0  # No match
        
        except:
            return 0
