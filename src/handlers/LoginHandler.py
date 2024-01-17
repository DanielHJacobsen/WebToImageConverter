from ..util.JsonExtraction import JsonExtraction as jsonExt
from ..util.ClickUtil import ClickUtil
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
import time

class LoginHandler:

    @staticmethod
    def login(driver, site, image_name, is_first_run):
        credentials = jsonExt.extract(site, "credentials", "", image_name, is_first_run)
        if credentials == "":
            return

        username = jsonExt.extract(credentials, "username", "", image_name, is_first_run)
        username_selector = jsonExt.extract(credentials, "username_selector", "", image_name, is_first_run)

        password = jsonExt.extract(credentials, "password", "", image_name, is_first_run)
        password_selector = jsonExt.extract(credentials, "password_selector", "", image_name, is_first_run)

        submit_selector = jsonExt.extract(credentials, "submit_selector", "", image_name, is_first_run)

        LoginHandler.send_keys_to_element(driver, input_value=username, selector=username_selector)
        LoginHandler.send_keys_to_element(driver, input_value=password, selector=password_selector)

        ClickUtil.click_element(submit_selector, driver)

        time.sleep(2)

    @staticmethod
    def send_keys_to_element(driver, input_value, selector):
        WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
        element = driver.find_element(By.CSS_SELECTOR, selector)
        element.send_keys(input_value)


