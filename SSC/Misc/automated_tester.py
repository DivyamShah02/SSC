from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from itertools import combinations

# Initialize WebDriver
driver = webdriver.Chrome(executable_path='path_to_chromedriver')
driver.get('http://yourwebsite.com/form')

def test_form_combinations():
    try:
        # Get all inputs, radios, checkboxes, and selects
        text_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        selects = driver.find_elements(By.TAG_NAME, 'select')

        # Fill text inputs (dummy values for now)
        for i, text_input in enumerate(text_inputs):
            text_input.clear()
            text_input.send_keys(f'TestValue{i}')
        
        # Handle all radio button combinations
        for radio in radio_buttons:
            radio.click()
            time.sleep(0.5)
            test_and_validate()

        # Handle all checkbox combinations (using combinations from itertools)
        checkbox_indices = range(len(checkboxes))
        for r in range(1, len(checkboxes) + 1):  # Length of subsets
            for subset in combinations(checkbox_indices, r):
                # Select only the current subset of checkboxes
                for checkbox in checkboxes:
                    if checkboxes.index(checkbox) in subset:
                        if not checkbox.is_selected():
                            checkbox.click()
                    else:
                        if checkbox.is_selected():
                            checkbox.click()
                time.sleep(0.5)
                test_and_validate()

        # Handle dropdown/select options
        for select in selects:
            dropdown = Select(select)
            for option in dropdown.options:
                dropdown.select_by_visible_text(option.text)
                time.sleep(0.5)
                test_and_validate()

    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        driver.quit()

def test_and_validate():
    """Submit the form and validate the result."""
    try:
        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()

        # Wait for redirection
        time.sleep(2)
        current_url = driver.current_url

        # Check if error occurred
        if 'error' in current_url.lower():
            print(f"Test failed! Redirected to error page: {current_url}")
        else:
            print(f"Test passed! Successfully redirected to: {current_url}")

        # Navigate back to reset the form for the next test
        driver.back()
        time.sleep(1)

    except Exception as e:
        print(f"Error during validation: {e}")

# Run the test
test_form_combinations()
