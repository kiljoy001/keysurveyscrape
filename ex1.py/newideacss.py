import unicodedata
from sys import argv
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import deque
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
import re
from itertools import cycle
from selenium.common.exceptions import TimeoutException

import time

# login to keysurvey

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
accum = 0

flist = driver.find_elements_by_css_selector("#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > *")
fqueue = deque(flist)
counter = list(fqueue)
for item in counter:
    # counter += 1
    element = WebDriverWait(driver, 20).until(
        lambda s: s.execute_script("return jQuery.active == 0"))
    if element:
        # Crashes here after 1 cycle
        ActionChains(driver).move_to_element(item).click(item).perform()
        branchPath = "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > li:nth-child({0})"
        # branchPath = "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > li:last-child > a"
        list2 = driver.find_elements_by_css_selector(
                "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > li"
            )
        queue = deque(list2)
        for each in range(1, len(queue)):
                print(len(list2))
                accum += 1

                element = WebDriverWait(driver, 20).until(
                    lambda s: s.execute_script("return jQuery.active == 0"))
                if element:
                    # selects next folder
                    nextFolder = driver.find_element_by_css_selector(branchPath.format(accum))
                    ActionChains(driver).click(nextFolder).perform()
                    intialFolder = driver.find_element_by_css_selector(branchPath.format(each)).click()
                    css_path = "#listContainer > ul > li:nth-child({0}) a"
                    element = WebDriverWait(driver, 20).until(
                        lambda s: s.execute_script("return jQuery.active == 0"))
                    if element:
                        # loop through survey folder list
                        subIndex = len(driver.find_elements_by_css_selector("#listContainer > ul a"))
                        for unit in range(1, subIndex + 1):
                            element = WebDriverWait(driver, 20).until(
                                lambda s: s.execute_script("return jQuery.active == 0"))
                            if element:
                                driver.find_element_by_css_selector(css_path.format(unit)).click()
                                csvElement = WebDriverWait(driver, 20).until(
                                    lambda s: s.execute_script("return jQuery.active == 0"))
                                if csvElement:
                                    csvClick = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.LINK_TEXT, "Export to CSV")))
                                    csvClick.click()
                                    csvRadioClick = WebDriverWait(driver, 20).until(
                                        lambda s: s.execute_script("return jQuery.active == 0"))
                                    # download phase
                                    if csvRadioClick:
                                        driver.execute_script("downloadExportWithLink(3,4);")
                                        javaCheck = WebDriverWait(driver, 20).until(
                                            EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                                        # double check to see if the reports link is clickable
                                        if javaCheck:
                                            checkagain = WebDriverWait(driver, 20).until(
                                                EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                                            if checkagain:
                                                reportsLink = driver.find_element_by_xpath("//*[@id='emptySel']/a")
                                                ActionChains(driver).move_to_element(reportsLink).click(
                                                    reportsLink).perform()
                        list2 = driver.find_elements_by_css_selector(
                            "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > li")
                        queue = deque(list2)

        fqueue.clear()
        flist = driver.find_elements_by_css_selector(
                    "#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > *")
        fqueue = deque(flist)
        fqueue.pop()
        counter = list(fqueue)

    else:
        continue