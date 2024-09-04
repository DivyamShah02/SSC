import pdb
import json
from library.Config import Config


class Sorter:
    def __init__(self) -> None:
        config_path = 'sorting_config.ini'
        self.config = Config(filename=config_path)

    def update_client_preferences(self, client_data):
        updated_data = client_data.copy()

        # Carpet area: keep variation of 15% on both sides of the range
        carpet_area_variation = float(self.config.client_data_variation.carpet_area_variation)
        min_carpet_area = float(client_data['min_carpet_area'])
        updated_data['min_carpet_area'] = min_carpet_area * (1 + (carpet_area_variation/100))

        # Budget:
        min_budget = float(client_data['budget_min'])
        max_budget = float(client_data['budget_max'])
        
        decision_driven = client_data.get('decision_driven_by')
        if decision_driven == 'budget':
            budget_variation = float(self.config.client_data_variation.budget_variation_budget_driven)
            updated_data['budget_min'] = min_budget * (1 + (budget_variation/100))
            updated_data['budget_max'] = max_budget * (1 + (budget_variation/100))
        elif decision_driven == 'choice':
            min_variation = float(self.config.client_data_variation.budget_variation_choice_driven_min)
            max_variation = float(self.config.client_data_variation.budget_variation_choice_driven_max)
            updated_data['budget_min'] = min_budget * (1 + (min_variation/100))
            updated_data['budget_max'] = max_budget * (1 + (max_variation/100))

        # Timeline: add 15% in the time on the higher side
        if 'time_to_seal_deal' in client_data:
            timeline_variation = float(self.config.client_data_variation.timeline_variation)
            timeline_value = int(client_data['time_to_seal_deal'])  # Assuming value is in months
            updated_data['time_to_seal_deal'] = int(timeline_value * (1 + (timeline_variation/100)))

        # Returning updated data as JSON
        return json.dumps(updated_data, indent=4)




if __name__ == '__main__':
    sorter = Sorter()
    client_details = {
        "min_carpet_area": "1200",
        "budget_min": "1",
        "budget_max": "1.5",
        "decision_driven_by": "budget",
        "time_to_seal_deal": "12"
    }

    updated_details = sorter.update_client_preferences(client_details)
    print(updated_details)
    print(sorter.config.client_data_variation.carpet_area_variation)
