import unicodedata
from sys import argv
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from itertools import cycle
from selenium.common.exceptions import TimeoutException

import time

# login to keysurvey
# driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# driver = webdriver.Chrome(executable_path=r'C:\phantomjs-2.1.1-windows\bin\chromedriver.exe')
driver = webdriver.Chrome(executable_path=r'C:\ProgramData\chocolatey\lib\chromedriver\tools\chromedriver.exe')


def execute_click(WebDriver, string):
    """

    :param WebDriver: Selenium webdriver
    :param string: css selector to the item to be clicked on
    :return: returns void
    """

    element = WebDriverWait(WebDriver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, string)))
    element.click()
    return


# driver = webdriver.Chrome(executable_path=r'E:\Projects\chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
eleUsername = driver.find_element_by_id("login")
elePassword = driver.find_element_by_id("password")
eleUsername.send_keys("kiljoy001@gmail.com")
elePassword.send_keys("$Master001")
# eleUsername.send_keys("RTCResearch@rtc.edu")
# elePassword.send_keys("R3search1")
driver.find_element_by_id("loginButton").click()
# https://app.keysurvey.com/app/action/Home/view/main/
# select reports link
driver.maximize_window()
driver.find_element_by_xpath("//a[@href='/Member/ReportWizard/dashboard.do ']").click()
print(driver.current_url)
# open main link

main = driver.find_element_by_css_selector("#main")
main.click()

list = driver.find_elements_by_css_selector("#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > *")

print("list of top level items: ", len(list))
topLevel = {}
# counter keeps track of the folder
counter = 0
for item in list:
    counter += 1
    print("Top Level:", counter, item.text)
    topLevel[item.get_attribute("id")] = item.get_attribute("title")
    element = WebDriverWait(driver, 20).until(
        lambda s: s.execute_script("return jQuery.active == 0"))
    if element:
        ActionChains(driver).move_to_element(item).click(item).perform()
    else:
        continue


# keeps track of the subfolder
subCounter = 0
subLevel = {}
for item in list:
    # folder match - if the counter is the same then then subitems are in the same folder
    subCounter += 1
    list2 = item.find_elements_by_css_selector("ul > *")
    subLevel[item.get_attribute("id")] = item.get_attribute("title")
    for each in list2:
        print("List 2:", subCounter, each.text)
        element = WebDriverWait(driver, 20).until(
            lambda s: s.execute_script("return jQuery.active == 0"))
        if element:
            ActionChains(driver).move_to_element(each).click(each).perform()
        else:
            continue



