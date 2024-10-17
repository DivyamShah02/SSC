from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

class SeleniumAutomation:
    def __init__(self):
        # Initialize the WebDriver with Chrome
        self.driver = None

    def start_chrome(self):
        """Starts the Chrome browser and sets up the WebDriver."""
        # Automatically download and use the latest ChromeDriver
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')  # Optional: Run Chrome in headless mode

        # Initialize the Chrome driver with options
        self.driver = webdriver.Chrome(service=service, options=options)
        print("Chrome browser started.")

    def get_url(self, url):
        """Navigates to the specified URL."""
        if self.driver:
            self.driver.get(url)
            print(f"Navigated to {url}")
        else:
            print("Driver not initialized. Call start_chrome() first.")

    def close_browser(self):
        """Closes the browser and quits the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")
        else:
            print("Driver not initialized.")

# Usage example
if __name__ == "__main__":
    automation = SeleniumAutomation()
    automation.start_chrome()
    automation.get_url("https://www.dynamiclabz.net/")
    # Perform additional actions here
    time.sleep(200)
    automation.close_browser()
