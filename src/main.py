import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import json
import os
import time
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

    def start(self):
        IntroPrint().print_ascii_art()

        config = self.load_config_file()

        location = self.jsonExt.extract_with_failure(config, "image_directory", "config")

        self.delete_old_files(location)

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.fullscreen_window()
        driver.maximize_window()

        self.start_screenshot_collection_and_slideshow(config, driver, location)

    @staticmethod
    def load_config_file():
        file = open("../config.json")
        try:
            config = json.load(file)
        except json.decoder.JSONDecodeError:
            print("Syntax issues found in the config.json file.")
            sys.exit()
        return config

    def start_screenshot_collection_and_slideshow(self, config, driver, location):
        self.collect_screenshots(config, driver, location)
        self.run_slide_show(config, driver, location)
        self.is_first_run = False
        self.start_screenshot_collection_and_slideshow(config, driver, location)

    def run_slide_show(self, config, driver, location):
        refresh_interval = self.jsonExt.extract(config, "refresh_interval", 5, "refresh_interval", self.is_first_run)

        for interation in range(refresh_interval):
            self.loop_slide_show(config, driver, location)

    def loop_slide_show(self, config, driver, location):
        time_per_slide = self.jsonExt.extract(config, "time_per_slide", 5, "config", self.is_first_run)

        for site in config["websites"]:
            image_name_with_format = site["image_name"] + ".png"
            try:
                driver.get(location + "/" + image_name_with_format)
            except NoSuchWindowException as e:
                print(e.msg)
                print("Was the program terminated manually?")
                sys.exit()

            time.sleep(time_per_slide)

    def collect_screenshots(self, config, driver, location):
        websites = self.jsonExt.extract_with_failure(config, "websites", "config")
        for site in websites:
            self.collect_snapshot(driver, location, site)

    def collect_snapshot(self, driver, location, site):
        image_name = self.jsonExt.extract_with_failure(site, "image_name", "websites")
        image_name_with_format = image_name + ".png"
        site_url = self.jsonExt.extract_with_failure(site, "url", image_name)
        driver.get(site_url)
        image_path = location + "/" + image_name_with_format

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

    @staticmethod
    def delete_old_files(location):
        for filename in os.listdir(location):
            if os.path.isfile(os.path.join(location, filename)) and filename.endswith(".png"):
                os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    Main().start()
