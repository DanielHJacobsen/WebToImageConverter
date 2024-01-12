from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import json
import os
import time

from selenium.webdriver.support.wait import WebDriverWait


def start():
    file = open("../config.json")
    config = json.load(file)
    location = config["image_directory"]

    delete_old_files(location)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.fullscreen_window()
    driver.maximize_window()

    start_screenshot_collection_and_slideshow(config, driver, location)


def start_screenshot_collection_and_slideshow(config, driver, location):
    collect_screenshots(config, driver, location)
    run_slide_show(config, driver, location)
    start_screenshot_collection_and_slideshow(config, driver, location)


def run_slide_show(config, driver, location):
    refresh_interval = extract_value_from_json(config, "refresh_interval", 5, "refresh_interval")

    for x in range(refresh_interval):
        loop_slide_show(config, driver, location)


def loop_slide_show(config, driver, location):
    time_per_slide = extract_value_from_json(config, "time_per_slide", 5, "time_per_slide")

    for site in config["websites"]:
        image_name_with_format = site["image_name"] + ".png"
        driver.get(location + "/" + image_name_with_format)
        time.sleep(time_per_slide)


def collect_screenshots(config, driver, location):
    for site in config["websites"]:
        image_name_with_format = site["image_name"] + ".png"

        driver.get(site["url"])
        selector = site["selector"]

        is_scroll_to_selector = extract_value_from_json(site, "scroll_to_selector", "false", site["image_name"])

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


def extract_value_from_json(json_object, key, default_value, object_reference):
    is_scroll_to_selector = default_value
    try:
        is_scroll_to_selector = json_object[key]
    except KeyError as e:
        print('There is no ' + key + '-property for the "' + object_reference + '" site.')
    return is_scroll_to_selector


def delete_old_files(location):
    for filename in os.listdir(location):
        if os.path.isfile(os.path.join(location, filename)):
            os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    start()
