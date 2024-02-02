import sys

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from util.Config import Config


class ClickUtil:

    @staticmethod
    def click_element(click_selector, driver):
        WebDriverWait(driver, Config().timeout).until(
            presence_of_element_located((By.CSS_SELECTOR, click_selector)))
        element = driver.find_element(By.CSS_SELECTOR, click_selector)
        try:
            element.click()
        except StaleElementReferenceException:
            ClickUtil.click_element(click_selector, driver)
        except TimeoutException:
            print('The CSS selector: "' + click_selector +
                  '" was not found within the configured '
                  '"allowed_timeout"-configuration ("' +
                  str(Config().timeout) + '" seconds).')
            sys.exit()
