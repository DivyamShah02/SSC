import os
import pdb
import json
from .library.Config import Config
from Property.models import BuildingDetails, UnitDetails, Amenities
from ClientDetail.models import PropertyInquiry
from ClientDetail.serializers import PropertyInquirySerializer
from SSC.settings import BASE_DIR


class Sorter:
    def __init__(self) -> None:
        config_path = os.path.join(BASE_DIR, 'SorterSession', 'sorting_config.ini')
        print(config_path)
        self.config = Config(filename=config_path)

    def update_client_preferences(self, client_data):
        updated_data = client_data.copy()

        # Carpet area: keep variation of 15% on both sides of the range
        carpet_area_variation = float(self.config.client_data_variation.carpet_area_variation)
        min_carpet_area = float(client_data['min_carpet_area'])
        updated_data['min_carpet_area'] = min_carpet_area * (1 + (carpet_area_variation/100))

        # Budget:
        min_budget = float(client_data['budget_min']) * 10000000
        max_budget = float(client_data['budget_max']) * 10000000

        decision_driven = client_data.get('decision_driven_by')
        if decision_driven == 'budget_driven':
            budget_variation = float(self.config.client_data_variation.budget_variation_budget_driven)
            updated_data['budget_min'] = min_budget * (1 + (budget_variation/100))
            updated_data['budget_max'] = max_budget * (1 + (budget_variation/100))
        elif decision_driven == 'choice_driven':
            min_variation = float(self.config.client_data_variation.budget_variation_choice_driven_min)
            max_variation = float(self.config.client_data_variation.budget_variation_choice_driven_max)
            updated_data['budget_min'] = min_budget * (1 + (min_variation/100))
            updated_data['budget_max'] = max_budget * (1 + (max_variation/100))

        # Timeline: add 15% in the time on the higher side
        if 'time_to_seal_deal' in client_data:
            timeline_variation = float(self.config.client_data_variation.timeline_variation)
            timeline_value = int(client_data['time_to_seal_deal'])  # Assuming value is in months
            updated_data['time_to_seal_deal'] = int(timeline_value * (1 + (timeline_variation/100)))

        bedrooms_list = client_data["bedrooms"].split(', ')

        formatted_bedrooms = [b.replace('_bhk', 'BHK').upper() for b in bedrooms_list]

        updated_data["bedrooms"] = ' | '.join(formatted_bedrooms)
        
        # Returning updated data as JSON
        return updated_data

    def get_pre_validated_property(self, update_client_data):
        validated_property = []

        bedrooms = update_client_data['bedrooms'].split(' | ')
        min_carpet_area = update_client_data['min_carpet_area']
        budget_min = update_client_data['budget_min']
        budget_max = update_client_data['budget_max']

        for bedroom in bedrooms:
            unit_type = 'Simplex'
            matching_properties = BuildingDetails.objects.filter(type_of_apartments__icontains=bedroom)
            for match_ in matching_properties:
                property_unit_matched = UnitDetails.objects.filter(building_id=match_.building_id, unit_configuration__icontains=bedroom, size_of_unit__gte=min_carpet_area, unit_type__icontains=unit_type)
                if len(property_unit_matched) !=0:
                    for property in property_unit_matched:
                        unit_price = property.size_of_unit * property.per_sqft_rate_saleable
                        if budget_min <= unit_price and budget_max >= unit_price:
                            validated_property.append(property)
        
        return validated_property

if __name__ == '__main__':
    pass
    # sorter = Sorter()
    # client_details = {
    #     "min_carpet_area": "1200",
    #     "budget_min": "1",
    #     "budget_max": "1.5",
    #     "decision_driven_by": "budget",
    #     "time_to_seal_deal": "12"
    # }

    # updated_details = sorter.update_client_preferences(client_details)
    # print(updated_details)
    # print(sorter.config.client_data_variation.carpet_area_variation)
