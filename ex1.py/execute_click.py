from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def execute_click(self, string):
    """
    Click on passed xpath element
    :param string: must be in XPath format
    :return: none
    """

    element = WebDriverWait(self.driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, string)))
    element.click()
    return