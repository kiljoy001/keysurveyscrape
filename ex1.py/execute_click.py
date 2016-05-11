from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def execute_click(WebDriver, string):
    """

    :param WebDriver: Selenium webdriver
    :param string: xpath to the item to be clicked on
    :return: returns void
    """

    element = WebDriverWait(WebDriver, 5).until(
    EC.element_to_be_clickable((By.XPATH, string)))
    element.click()
    return