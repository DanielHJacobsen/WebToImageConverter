import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import json
import os
import time

from src.util.Config import Config
from src.util.IntroUtil import IntroPrint
from src.handlers.CaptionHandler import CaptionHandler
from src.handlers.NavigationHandler import NavigationHandler
from src.handlers.LoginHandler import LoginHandler
from src.util.JsonExtraction import JsonExtraction


class Main:
    is_first_run = True
    captionHandler = CaptionHandler()
    navigationHandler = NavigationHandler()
    loginHandler = LoginHandler()
    jsonExt = JsonExtraction()
    config = Config()

    def start(self):
        IntroPrint().print_ascii_art()

        config_file = self.load_config_file()

        self.setup_configuration_util(config_file)

        self.delete_old_files()

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.fullscreen_window()
        driver.maximize_window()

        self.start_screenshot_collection_and_slideshow(config_file, driver)

    @staticmethod
    def load_config_file():
        try:
            file = open("../config.json")
        except FileNotFoundError:
            print("No 'config.json' file was found in the root of the repository.")
            sys.exit()
        try:
            config = json.load(file)
        except json.decoder.JSONDecodeError:
            print("Syntax issues found in the config.json file.")
            sys.exit()
        return config

    def setup_configuration_util(self, config_file):
        location = self.jsonExt.extract_with_failure(config_file, "image_directory", "config_file")
        timeout = self.jsonExt.extract(config_file, "allowed_timeout", 5, "config_file", True)
        refresh_interval = self.jsonExt.extract(config_file, "refresh_interval", 5, "refresh_interval", True)
        time_per_slide = self.jsonExt.extract(config_file, "time_per_slide", 5, "time_per_slide", True)

        self.config.location = location
        self.config.timeout = timeout
        self.config.time_per_slide = time_per_slide
        self.config.refresh_interval = refresh_interval

    def start_screenshot_collection_and_slideshow(self, config, driver):
        self.collect_screenshots(config, driver)
        self.run_slide_show(config, driver)
        self.is_first_run = False
        self.start_screenshot_collection_and_slideshow(config, driver)

    def run_slide_show(self, config, driver):
        for interation in range(self.config.refresh_interval):
            self.loop_slide_show(config, driver, interation)

    def loop_slide_show(self, config, driver, interation):
        for site in config["websites"]:
            if not self.is_screenshot_iteration(interation, site):
                continue

            image_name_with_format = site["image_name"] + ".png"
            try:
                path = self.config.location + "/" + image_name_with_format
                file_exits = os.path.exists(path)

                if file_exits:
                    self.handle_existing_image(driver, path)
                else:
                    self.handle_missing_image(path, site)

            except NoSuchWindowException as e:
                print(e.msg)
                print("Was the program terminated manually? - If so, don't worry about this log.")
                sys.exit()

    def is_screenshot_iteration(self, interation, site):
        show_for_every_x_iteration = self.jsonExt.extract(site,
                                                          "show_for_every_x_interation",
                                                          1,
                                                          "websites",
                                                          self.is_first_run)
        return ((interation + 1) % show_for_every_x_iteration) == 0

    def handle_existing_image(self, driver, path):
        driver.get(path)
        self.timeout_on_screenshot()

    def timeout_on_screenshot(self):
        # noinspection PyBroadException
        try:
            time.sleep(self.config.time_per_slide)
        except:
            print("Was the program terminated manually? - If so, don't worry about this log.")
            sys.exit()

    def handle_missing_image(self, path, site):
        print('There was found no file with the path "' + path + '"')
        skip_if_failed = self.jsonExt.extract(site, "skip_if_failed", True, "websites", self.is_first_run)
        if skip_if_failed:
            print('The website was configured as "skip_if_failed" and '
                  'the website will therefore be skipped.')
        else:
            print('The website was configured as not "skip_if_failed" and '
                  'the failure shall therefore cause termination of the program.')
            sys.exit()

    def collect_screenshots(self, config, driver):
        websites = self.jsonExt.extract_with_failure(config, "websites", "config")
        for site in websites:
            self.collect_snapshot(driver, site)

    def collect_snapshot(self, driver, site):
        skip_if_failed = self.jsonExt.extract(site, "skip_if_failed", True, "websites", self.is_first_run)
        # noinspection PyBroadException
        try:
            image_name = self.jsonExt.extract_with_failure(site, "image_name", "websites")
            image_name_with_format = image_name + ".png"
            site_url = self.jsonExt.extract_with_failure(site, "url", image_name)
            driver.get(site_url)
            image_path = self.config.location + "/" + image_name_with_format

            self.loginHandler.login(driver=driver,
                                    site=site,
                                    image_name=image_name,
                                    is_with_log=self.is_first_run)

            self.navigationHandler.navigate(driver=driver,
                                            site=site,
                                            image_name=image_name,
                                            image_path=image_path,
                                            is_with_log=self.is_first_run)

            self.captionHandler.add_caption(site=site,
                                            image_path=image_path,
                                            is_with_log=self.is_first_run)
        except:
            print('The website "' + image_name + '" failed due to an undefined error.')
            if skip_if_failed:
                print('The website will therefore be skipped.')
            else:
                print('The website was configured as not "skip_if_failed" and '
                      'the failure shall therefore cause termination of the program.')
                sys.exit()

    def delete_old_files(self):
        location = self.config.location

        for filename in os.listdir(location):
            if os.path.isfile(os.path.join(location, filename)) and filename.endswith(".png"):
                os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    Main().start()
