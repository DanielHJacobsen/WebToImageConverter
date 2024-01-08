
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import json
import os
import time

from selenium.webdriver.support.wait import WebDriverWait


def main():
    file = open("config.json")
    config = json.load(file)
    location = config["image_directory"]

    delete_old_files(location)

    driver = webdriver.Chrome()
    driver.maximize_window()

    collect_screenshots(config, driver, location)

    driver.fullscreen_window()
    driver.maximize_window()
    run_slide_show(config, driver, location)


def run_slide_show(config, driver, location):
    loop_slide_show(config, driver, location)
    run_slide_show(config, driver, location)


def loop_slide_show(config, driver, location):
    for site in config["websites"]:
        image_name_with_format = site["image_name"] + ".png"
        driver.get(location + "/" + image_name_with_format)
        time.sleep(10)


def collect_screenshots(config, driver, location):
    for site in config["websites"]:
        image_name_with_format = site["image_name"] + ".png"

        driver.get(site["url"])
        selector = site["selector"]

        if selector != "":
            WebDriverWait(driver, 10).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
            element = driver.find_element(By.CSS_SELECTOR, selector)
            element.screenshot(location + "/" + image_name_with_format)

        else:
            driver.save_screenshot(location + "/" + image_name_with_format)


def delete_old_files(location):
    for filename in os.listdir(location):
        if os.path.isfile(os.path.join(location, filename)):
            os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    main()
