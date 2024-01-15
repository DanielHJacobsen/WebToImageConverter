import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from ..util.JsonExtraction import JsonExtraction as jsonExt
from selenium.webdriver.support.wait import WebDriverWait


class NavigationHandler:

    @staticmethod
    def navigate_for_screenshot(driver, image_name, image_path, site, is_first_run):
        selector = jsonExt.extract(site, "selector", "", image_name, is_first_run)
        is_scroll_to_selector = jsonExt.extract(site, "scroll_to_selector", False, image_name, is_first_run)
        clicks = jsonExt.extract(site, "clicks", [], image_name, is_first_run)
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
