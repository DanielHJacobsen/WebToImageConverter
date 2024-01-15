import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import json
import os
import time
from IntroPrint import IntroPrint
from CaptionHandler import CaptionHandler
from JsonExtraction import JsonExtraction

from selenium.webdriver.support.wait import WebDriverWait


class Main:
    is_first_run = True
    captionHandler = CaptionHandler()
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

        for x in range(refresh_interval):
            self.loop_slide_show(config, driver, location)

    def loop_slide_show(self, config, driver, location):
        time_per_slide = self.jsonExt.extract(config, "time_per_slide", 5, "config", self.is_first_run)

        for site in config["websites"]:
            image_name_with_format = site["image_name"] + ".png"
            driver.get(location + "/" + image_name_with_format)
            time.sleep(time_per_slide)

    def collect_screenshots(self, config, driver, location):
        websites = self.jsonExt.extract_with_failure(config, "websites", "config")
        for site in websites:
            image_name = self.jsonExt.extract_with_failure(site, "image_name", "websites")
            image_name_with_format = image_name + ".png"

            site_url = self.jsonExt.extract_with_failure(site, "url", image_name)
            driver.get(site_url)
            selector = self.jsonExt.extract(site, "selector", "", image_name, self.is_first_run)

            is_scroll_to_selector = self.jsonExt.extract(site, "scroll_to_selector", False, image_name, self.is_first_run)

            clicks = self.jsonExt.extract(site, "clicks", [], image_name, self.is_first_run)

            image_path = location + "/" + image_name_with_format
            if selector != "" and not is_scroll_to_selector:
                WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.screenshot(image_path)

            elif selector != "" and is_scroll_to_selector:
                WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
                selector.replace("\"", "'")
                script = 'window.scroll(0,document.querySelector("' + selector + '").getBoundingClientRect().y)'
                driver.execute_script(script)
                driver.save_screenshot(image_path)

            elif clicks:
                for click_selector in clicks:
                    print(click_selector)
                    WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, click_selector)))
                    element = driver.find_element(By.CSS_SELECTOR, click_selector)
                    element.click()

                time.sleep(2)
                driver.save_screenshot(image_path)

            else:
                driver.save_screenshot(image_path)

            self.captionHandler.add_caption_to_image(site, image_path, self.is_first_run)

    @staticmethod
    def delete_old_files(location):
        for filename in os.listdir(location):
            if os.path.isfile(os.path.join(location, filename)) and filename.endswith(".png"):
                os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    Main().start()
