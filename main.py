from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os


def main():
    file = open("config.json")
    config = json.load(file)
    location = config["image_directory"]

    delete_old_files(location)

    driver = webdriver.Chrome()
    driver.maximize_window()

    collect_screenshots(config, driver, location)


def collect_screenshots(config, driver, location):
    for site in config["websites"]:
        image_name_with_format = site["image_name"] + ".png"

        driver.get(site["url"])
        selector = site["selector"]
        if selector != "":
            driver.find_element(By.CSS_SELECTOR, selector)

        driver.save_screenshot(location + "/" + image_name_with_format)
    driver.close()


def delete_old_files(location):
    for filename in os.listdir(location):
        if os.path.isfile(os.path.join(location, filename)):
            os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    main()
