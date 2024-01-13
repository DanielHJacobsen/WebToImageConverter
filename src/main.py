import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import json
import os
import time
from IntroPrint import IntroPrint

from selenium.webdriver.support.wait import WebDriverWait


class Main:
    is_first_run = True

    def start(self):
        IntroPrint().print_ascii_art()

        config = self.load_config_file()

        location = self.extract_value_from_json_with_failure(config, "image_directory", "config")

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
        refresh_interval = self.extract_value_from_json(config, "refresh_interval", 5, "refresh_interval")

        for x in range(refresh_interval):
            self.loop_slide_show(config, driver, location)

    def loop_slide_show(self, config, driver, location):
        time_per_slide = self.extract_value_from_json(config, "time_per_slide", 5, "config")

        for site in config["websites"]:
            image_name_with_format = site["image_name"] + ".png"
            driver.get(location + "/" + image_name_with_format)
            time.sleep(time_per_slide)

    def collect_screenshots(self, config, driver, location):
        websites = self.extract_value_from_json_with_failure(config, "websites", "config")
        for site in websites:
            image_name = self.extract_value_from_json_with_failure(site, "image_name", "websites")
            image_name_with_format = image_name + ".png"

            site_url = self.extract_value_from_json_with_failure(site, "url", image_name)
            driver.get(site_url)
            selector = self.extract_value_from_json(site, "selector", "", image_name)

            is_scroll_to_selector = self.extract_value_from_json(site, "scroll_to_selector", False, image_name)

            if selector != "" and not is_scroll_to_selector:
                WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.screenshot(location + "/" + image_name_with_format)

            elif selector != "" and is_scroll_to_selector:
                WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
                selector.replace("\"", "'")
                script = 'window.scroll(0,document.querySelector("' + selector + '").getBoundingClientRect().y)'
                driver.execute_script(script)
                driver.save_screenshot(location + "/" + image_name_with_format)

            else:
                driver.save_screenshot(location + "/" + image_name_with_format)

    def extract_value_from_json(self, json_object, key, default_value, object_reference):
        is_scroll_to_selector = default_value
        try:
            is_scroll_to_selector = json_object[key]
        except KeyError:
            if self.is_first_run:
                print('There is no ' + key + '-property for the "' + object_reference + '"-object.')
        return is_scroll_to_selector

    @staticmethod
    def extract_value_from_json_with_failure(json_object, key, object_reference):
        try:
            return json_object[key]
        except KeyError:
            print('The required key of ' + key + ' is missing for the "' + object_reference + '"-object.')
            sys.exit()

    @staticmethod
    def delete_old_files(location):
        for filename in os.listdir(location):
            if os.path.isfile(os.path.join(location, filename)):
                os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    Main().start()
