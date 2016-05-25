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
branch_css_path = "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > li.open.activS > ul >" \
                  " li:nth-child({0}) a"
tree_css_path = "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > li:nth-child({0}) a"
css_path = "#listContainer > ul > li:nth-child({0}) a"
surveyXP = "//*[@id='treeContainer']//a[starts-with(@id, 's')]"
standReport = "//*[@id='treeContainer']//a[@id='r-1']"
treeList = "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul a"
topList = len(driver.find_elements_by_css_selector(treeList))

# print("list of top level items: ", len(list))
topLevel = {}
# counter keeps track of the folder
counter = 0
for item in range(1, topList):
    counter += 1
    # print("Top Level:", counter, item.text)
    # topLevel[item.get_attribute("id")] = item.get_attribute("title")
    element = WebDriverWait(driver, 20).until(
        lambda s: s.execute_script("return jQuery.active == 0"))
    if element:
        driver.find_element_by_css_selector(tree_css_path.format(item)).click()
    else:
        continue

# keeps track of the subfolder
subCounter = 0
subLevel = {}
for item in range(1, topList):
    # folder match - if the counter is the same then then subitems are in the same folder
    subCounter += 1
    list2 = len(driver.find_elements_by_css_selector(branch_css_path.format(item)))
    # subLevel[item.get_attribute("id")] = item.get_attribute("title")
    for each in range(1, list2):
        # print("List 2:", subCounter, each.text)
        element = WebDriverWait(driver, 20).until(
            lambda s: s.execute_script("return jQuery.active == 0"))
        if element:
            ActionChains(driver).move_to_element(each).click(each).perform()
            standReportList = driver.find_elements_by_xpath(standReport)
            sublist = driver.find_elements_by_xpath(surveyXP)
            for unit in standReportList:
                sublist.append(unit)
            totalSurvey = len(sublist)
            print("totalSurvey len: ", totalSurvey)
            for index in range(1, totalSurvey):
                element = WebDriverWait(driver, 20).until(
                    lambda s: s.execute_script("return jQuery.active == 0"))
                if element:
                    subIndex = len(driver.find_elements_by_css_selector("#listContainer > ul a"))
                print("subindex length: ", subIndex)
                for stuff in range(1, subIndex + 1):
                    element = WebDriverWait(driver, 20).until(
                        lambda s: s.execute_script("return jQuery.active == 0"))
                    if element:
                        driver.find_element_by_css_selector(css_path.format(stuff)).click()
                        csvElement = WebDriverWait(driver, 20).until(
                            lambda s: s.execute_script("return jQuery.active == 0"))
                        if csvElement:
                            csvClick = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.LINK_TEXT, "Export to CSV")))
                            csvClick.click()
                        csvRadioClick = WebDriverWait(driver, 20).until(
                            lambda s: s.execute_script("return jQuery.active == 0"))
                        if csvRadioClick:
                            driver.execute_script("downloadExportWithLink(3,4);")
                            javaCheck = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                            if javaCheck:
                                checkagain = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                                if checkagain:
                                    reportsLink = driver.find_element_by_xpath("//*[@id='emptySel']/a")
                                    ActionChains(driver).move_to_element(reportsLink).click(reportsLink).perform()
        else:
            continue


