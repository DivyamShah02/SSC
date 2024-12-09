import os
import sys
import pdb
import time

from library.Config import Config
from library.GetLogger import GetLogger
from library.ChromeHandler import ChromeHandler


class Runner:
    def __init__(self) -> None:
        self.start_time = time.time()

        cwd_path = os.getcwd()
        config_path = cwd_path.replace('DevFiles', 'BotConfig\\config.ini')
        self.config = Config(filename=config_path)

        logs_dir = self.config.paths.logs_path
        self.logger = GetLogger(log_file_dir=logs_dir, log_file_name="chrome_automater.log", file_handler=True).logger

        self.chrome_handler = ChromeHandler(logger=self.logger, config=self.config)
        self.start_and_max_chrome()

    def start_and_max_chrome(self):
        if not self.chrome_handler.start_chrome():
            self.logger.error("Failed to start Chrome.")
            sys.exit(1)

        if not self.chrome_handler.maximise_chrome():
            self.logger.error("Failed to maximize Chrome.")
            self.chrome_handler.kill_all_chrome()
            sys.exit(1)

    def run(self):
        if not self.chrome_handler.load_url(url=str(self.config.Selenium_Details.url).replace("'", '')):
            self.logger.error("Failed to load URL")

        if not self.chrome_handler.fullscreen_chrome():
            self.logger.error("Failed to fullscreen")

        self.chrome_handler.test_form_combinations()

        screenshot_path = self.generate_file_name(folder=self.config.paths.screenshot_path, file_name='screenshot.png')
        if not self.chrome_handler.take_screenshot(screenshot_path=screenshot_path):
            self.logger.error("Failed to take screenshot")

        self.end()
    
    def end(self):
        self.chrome_handler.quit_chrome()
        self.end_time = time.time()

        self.logger.info(f'# Total time taken: {self.end_time - self.start_time}')
        sys.exit()

    def generate_file_name(self, folder, file_name):
        """Generate unique file name to avoid conflicts."""
        process_file_path = os.path.join(folder, file_name)
        counter = 1
        while os.path.exists(process_file_path):
            base_name, ext = os.path.splitext(file_name)
            base_name = str(base_name).replace(f'_{counter-1}','')
            process_file_path = os.path.join(folder, f"{base_name}_{counter}{ext}")
            counter += 1
        return process_file_path

if __name__ == '__main__':
    runner = Runner()
    runner.run()
