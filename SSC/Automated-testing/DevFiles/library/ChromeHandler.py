import pdb
import time
from selenium import webdriver
from itertools import combinations
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException

from library.GetLogger import apply_logs_to_all_methods, log

@apply_logs_to_all_methods(log)
class ChromeHandler:
    def __init__(self, logger, config) -> None:
        self.logger = logger
        self.config = config
        self.driver = None
        # self.kill_all_chrome()

    def kill_all_chrome(self) -> None:
        """Terminate all Chrome processes."""
        try:
            self.logger.info("Terminating all Chrome processes.")
            # os.system("taskkill /F /IM chrome.exe")
            self.logger.info("All Chrome processes terminated.")
        except Exception as e:
            self.logger.error("Failed to terminate Chrome processes.", exc_info=True)

    def start_chrome(self) -> bool:
        """Start Chrome browser using Selenium."""
        try:
            self.logger.info("Starting Chrome with Selenium WebDriver.")
            chrome_options = Options()
            prefs = {
                "download.default_directory": self.config.paths.download_path,
                "download.prompt_for_download": False,
                "profile.default_content_settings.popups": 0,
                "directory_upgrade": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            # options.add_argument('--headless')  # Optional: Run Chrome in headless mode

            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            self.logger.info("Chrome started successfully.")
            return True
        except WebDriverException as e:
            self.logger.error("Error while starting Chrome with Selenium.", exc_info=True)
            return False

    def maximise_chrome(self) -> bool:
        """Maximize Chrome window."""
        try:
            self.logger.info("Maximizing Chrome window.")
            self.driver.maximize_window()
            self.logger.info("Chrome window maximized successfully.")
            return True
        except WebDriverException as e:
            self.logger.error("Error while maximizing Chrome window.", exc_info=True)
            return False

    def fullscreen_chrome(self) -> bool:
        """Maximize Chrome window."""
        try:
            self.logger.info("Turning Chrome to full screen window.")
            self.driver.fullscreen_window()
            self.logger.info("Chrome window fullscreened successfully.")
            return True
        except WebDriverException as e:
            self.logger.error("Error while fullscreening Chrome window.", exc_info=True)
            return False

    def load_url(self, url: str) -> bool:
        """Load a specific URL in Chrome."""
        try:
            self.logger.info(f"Loading URL: {url}")
            self.driver.get(url)
            self.logger.info(f"URL {url} loaded successfully.")
            time.sleep(20)
            return True
        except WebDriverException as e:
            self.logger.error(f"Error while loading URL: {url}", exc_info=True)
            return False

    def take_screenshot(self, screenshot_path: str) -> bool:
        """Takes screenshot and saves to the path passed in arg."""
        try:
            self.logger.info(f"Taking Screenshot")
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"Successfully saved screenshot to '{screenshot_path}'.")
            return True
        except WebDriverException as e:
            self.logger.error(f"Error while taking screenshot.", exc_info=True)
            return False

    def scroll_to_end_of_page(self) -> None:
        """Scroll to the end of the web page."""
        try:
            self.logger.info("Scrolling to the end of the page.")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.logger.info("Successfully scrolled to the end of the page.")
            return True
        except Exception as e:
            self.logger.error("Error occurred while scrolling to the end of the page.", exc_info=True)
            return False

    def click_button_by_xpath(self, xpath: str) -> bool:
        """Dynamically click on a button using the provided XPath."""
        try:
            self.driver.implicitly_wait(10)  # Optional: Implicit wait for the element to be present
            self.logger.info(f"Attempting to click button with XPath: {xpath}")
            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
            self.logger.info(f"Successfully clicked the button with XPath: {xpath}")
            return True
        except NoSuchElementException:
            self.logger.error(f"Element not found with XPath: {xpath}", exc_info=True)
            return False
        except ElementClickInterceptedException:
            self.logger.error(f"Element with XPath: {xpath} could not be clicked.", exc_info=True)
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while clicking the button with XPath: {xpath}", exc_info=True)
            return False

    def template_fun(self) -> bool:
        """Placeholder function for custom logic."""
        try:
            self.logger.info("Executing template function.")
            # Custom logic using Selenium goes here
            self.logger.info("Template function executed successfully.")
            return True
        except Exception as e:
            self.logger.error("Error while executing template function.", exc_info=True)
            return False

    def quit_chrome(self) -> None:
        """Quit Chrome browser."""
        try:
            self.logger.info("Quitting Chrome.")
            if self.driver:
                self.driver.quit()
            self.logger.info("Chrome quit successfully.")
        except WebDriverException as e:
            self.logger.error("Error while quitting Chrome.", exc_info=True)

    def test_form_combinations(self):
        try:
            # Get all inputs, radios, checkboxes, and selects
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
            radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
            selects = self.driver.find_elements(By.TAG_NAME, 'select')

            # Fill text inputs (dummy values for now)
            # for i, text_input in enumerate(text_inputs):
            #     text_input.clear()
            #     text_input.send_keys(f'TestValue{i}')
            
            # Handle all radio button combinations
            # for i in range(len(radio_buttons)):
            #     j = i
            #     latest_radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            #     radio = latest_radio_buttons[i]
            #     clicked = False
            #     try:
            #         radio.location_once_scrolled_into_view
            #         time.sleep(1)
            #         self.driver.execute_script("window.scrollBy(0, -200);")
            #         time.sleep(1)
            #         radio.click()                    
            #         print(f'Clicked {radio.accessible_name}')
            #         self.logger.info(f'Clicked {radio.accessible_name}')
            #         time.sleep(0.5)
            #         clicked = True
            #     except Exception as ex:
            #         print(f'error in {radio.accessible_name} =======================================================================')                    
            #         self.logger.error(f'error in {radio.accessible_name} =======================================================================')
            #         self.logger.error(ex, exc_info=True)

            #     if clicked:
            #         validated = self.test_and_validate(input_name=radio.accessible_name)
            #         while not validated:
            #             latest_radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            #             j = j-1
            #             radio = latest_radio_buttons[j]
            #             radio.location_once_scrolled_into_view
            #             time.sleep(1)
            #             self.driver.execute_script("window.scrollBy(0, -200);")
            #             time.sleep(1)
            #             radio.click()
            #             validated = self.test_and_validate(input_name=radio.accessible_name)

            #     # pdb.set_trace()

            # Handle all checkbox combinations (using combinations from itertools)
            checkbox_indices = range(len(checkboxes))
            for r in range(1, len(checkboxes) + 1):  # Length of subsets
                for subset in combinations(checkbox_indices, r):
                    # Select only the current subset of checkboxes
                    for checkbox in checkboxes:
                        pdb.set_trace()
                        if checkboxes.index(checkbox) in subset:
                            if not checkbox.is_selected():
                                checkbox.click()
                        else:
                            if checkbox.is_selected():
                                checkbox.click()
                    time.sleep(0.5)
            pdb.set_trace()
            self.test_and_validate()

            # # Handle dropdown/select options
            # for select in selects:
            #     dropdown = Select(select)
            #     for option in dropdown.options:
            #         dropdown.select_by_visible_text(option.text)
            #         time.sleep(0.5)
            #         self.test_and_validate()

        except Exception as e:
            print(f"Error during testing: {e}")
            self.logger.error(e, exc_info=True)
        finally:
            self.driver.quit()

    def test_and_validate(self, input_name):
        """Submit the form and validate the result."""
        try:
            time.sleep(1)
            self.scroll_to_end_of_page()
            time.sleep(1)
            # Submit the form
            # submit_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/form/div/div[7]/button')
            submit_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/form/div/div[17]/div[1]/button')
            submit_button.click()

            # Wait for redirection
            # time.sleep(15)
            time.sleep(5)
            
            success = self.get_result_property_detail(input_name=input_name)

            # # Get the handles for all open tabs
            # handles = self.driver.window_handles

            # # Switch to the new tab (second tab)
            # self.driver.switch_to.window(handles[1])

            # # Close the earlier tab (first tab)
            # self.driver.switch_to.window(handles[0])  # Switch to the first tab
            # self.driver.close()  # Close the first tab

            # # Switch back to the new tab (second tab)
            # self.driver.switch_to.window(handles[1])

            # time.sleep(4)

            return success


        except Exception as e:
            print(f"Error during validation: {e}")
            self.logger.error(e, exc_info=True)

    def get_result(self, input_name):
        current_url = self.driver.current_url
        self.logger.info(f'Clicked on {input_name} redirected to {current_url}')

        # Navigate back to reset the form for the next test
        new_tab_url = 'http://127.0.0.1:8000/property-inquiry/?client_id=1'
        self.driver.execute_script(f"window.open('{new_tab_url}', '_blank');")
        time.sleep(1)
        
        # Check if error occurred
        if 'error_page' in current_url.lower():
            print(f"Test failed! Redirected to error page: {current_url} while clicking on {input_name}")
            self.logger.info(f"Test failed! Redirected to error page: {current_url} while clicking on {input_name}")
            return False
        else:
            print(f"Test passed! Successfully redirected to: {current_url}")
            self.logger.info(f"Test passed! Successfully redirected to: {current_url}")
            return True

    def get_result_property_detail(self, input_name):
        # pdb.set_trace()
        # time.sleep(4)
        # Switch to the alert
        alert = self.driver.switch_to.alert

        # Get the text of the alert
        alert_text = alert.text
        print(f"The alert says: {alert_text}")

        alert.accept() 

        time.sleep(5)

        if 'successfully' not in alert_text.lower():
            print(f"Test failed! Redirected to error page: {alert_text} while clicking on {input_name}")
            self.logger.info(f"Test failed! Redirected to error page: {alert_text} while clicking on {input_name}")
            return False
        else:
            print(f"Test passed! Successfully redirected to: {alert_text}")
            self.logger.info(f"Test passed! Successfully redirected to: {alert_text}")
            return True

