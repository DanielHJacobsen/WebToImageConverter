from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class ClickUtil:

    @staticmethod
    def click_element(click_selector, driver):
        WebDriverWait(driver, 5).until(presence_of_element_located((By.CSS_SELECTOR, click_selector)))
        element = driver.find_element(By.CSS_SELECTOR, click_selector)
        try:
            element.click()
        except StaleElementReferenceException:
            ClickUtil.click_element(click_selector, driver)
