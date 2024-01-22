import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import TimeoutException

from ..util.Config import Config
from ..util.JsonExtraction import JsonExtraction as jsonExt
from selenium.webdriver.support.wait import WebDriverWait
from ..util.ClickUtil import ClickUtil


class NavigationHandler:

    @staticmethod
    def navigate(driver, image_name, image_path, site, is_with_log):
        selector = jsonExt.extract(site, "selector", "", image_name, is_with_log)
        is_scroll_to_selector = jsonExt.extract(site, "scroll_to_selector", False, image_name, is_with_log)
        clicks = jsonExt.extract(site, "clicks", [], image_name, is_with_log)
        if selector != "" and not is_scroll_to_selector:
            NavigationHandler.selector_cutting_navigation(driver, image_path, selector)

        elif selector != "" and is_scroll_to_selector:
            NavigationHandler.selector_scrolling_navigation(driver, image_path, selector)

        elif clicks:
            NavigationHandler.click_navigation(clicks, driver, image_path)

        else:
            driver.save_screenshot(image_path)

    @staticmethod
    def click_navigation(clicks, driver, image_path):
        for click_selector in clicks:
            try:
                ClickUtil.click_element(click_selector, driver)
            except TimeoutException:
                print('The CSS selector: "' + click_selector +
                      '" was not found within the configured '
                      '"allowed_timeout"-configuration ("' +
                      Config().timeout + '" seconds).')
                sys.exit()

        time.sleep(2)
        driver.save_screenshot(image_path)

    @staticmethod
    def selector_scrolling_navigation(driver, image_path, selector):
        WebDriverWait(driver, Config().timeout).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
        selector.replace("\"", "'")
        script = 'window.scroll(0,document.querySelector("' + selector + '").getBoundingClientRect().y)'
        driver.execute_script(script)
        driver.save_screenshot(image_path)

    @staticmethod
    def selector_cutting_navigation(driver, image_path, selector):
        try:
            WebDriverWait(driver, Config().timeout).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
            element = driver.find_element(By.CSS_SELECTOR, selector)
            element.screenshot(image_path)
        except TimeoutException:
            print('The CSS selector: "' + selector +
                  '" was not found within the configured '
                  '"allowed_timeout"-configuration ("' +
                  Config().timeout + '" seconds).')
            sys.exit()
