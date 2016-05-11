
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
#login to keysurvey
#driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver = webdriver.Chrome(executable_path=r'C:\phantomjs-2.1.1-windows\bin\chromedriver.exe')
#driver = webdriver.Chrome(executable_path=r'E:\Projects\chromedriver.exe')
driver.implicitly_wait(5)
driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
eleUsername = driver.find_element_by_id("login")
elePassword = driver.find_element_by_id("password")
eleUsername.send_keys("RTCResearch@rtc.edu")
elePassword.send_keys("R3search1")
driver.find_element_by_id("loginButton").click()
#https://app.keysurvey.com/app/action/Home/view/main/
#select reports link
driver.maximize_window()
driver.find_element_by_xpath("//a[@href='/Member/ReportWizard/dashboard.do ']").click()
print(driver.current_url)
#https://app.keysurvey.com/app/action/report/Home/view/custom/
#open main link
element = WebDriverWait(driver, 1).until(
EC.element_to_be_clickable((By.XPATH, "//*[@id='main']")))
element.click()

#element = WebDriverWait(driver, 1).until(
#EC.element_to_be_clickable((By.XPATH, "//*[@id='treeContainer']/ul/li[2]/ul//li")))
list = driver.find_elements_by_xpath("//*[@id='treeContainer']//a[starts-with(@id, 'f')]")
print("list of top level items: ",len(list))
topLevel ={}
for item in list:
    topLevel[item.get_attribute("id")] = item.get_attribute("title")
    ActionChains(driver).move_to_element(item).click(item).perform()
print("length of topLevel dictionary: ", len(topLevel))
secondLevel ={}
secondLevelList = driver.find_elements_by_xpath("//*[@id='treeContainer']//a[starts-with(@id, 'f')]")
secondLevelList.append(driver.find_element(By.ID, "strash"))
print("list of second level items: ",len(secondLevelList))
for item in secondLevelList:
    if item.get_attribute("id") in topLevel:
        pass
    else:
        secondLevel[item.get_attribute("id")] = item.get_attribute("title")
        ActionChains(driver).move_to_element(item).click(item).perform()

check = driver.find_elements_by_class_name("surveyFolder")
check.append(driver.find_element(By.ID, "strash"))
print("items in check list: ", len(check))
#many items does not seem to be clicked constantly, added below to make sure it gets clicked on
for item in check:
    ActionChains(driver).move_to_element(item).click(item).perform()
    if item.get_attribute("id") in secondLevelList:
        pass
    else:
        secondLevel[item.get_attribute("id")] = item.get_attribute("title")
print("length of secondlvl dictionary: ", len(secondLevel))
#gather survey items
surveyList = driver.find_elements_by_xpath("//*[@id='treeContainer']//a[starts-with(@id, 's')]")
print("number of surveys found: ", len(surveyList))
surveyDict = {}
counter = 0
for item in surveyList:
    if item.get_attribute("id") in surveyDict:
        pass
    elif item.get_attribute("title") == "Close":
        pass
    else:
        surveyDict[item.get_attribute("id")] = item.get_attribute("title")
        ActionChains(driver).move_to_element(item).click(item).perform()
        counter+=1
        print(counter, item.get_attribute("title"))
print("length of dictionary list: ", len(surveyDict))
subSurveyDict = {}
subSurveyList = driver.find_elements_by_xpath("//*[@id='treeContainer']//a[starts-with(@id, 'f')]")
for item in subSurveyList:
    if item.get_attribute("id") in topLevel or item.get_attribute("id") in secondLevel:
        pass
    else:
        subSurveyDict[item.get_attribute("id")] = item.get_attribute("title")
print("number of items in subSurvey dict", len(subSurveyDict))
bsObj = BeautifulSoup(driver.page_source, "html.parser")
for child in bsObj.recursiveChildGenerator():
    title = getattr(child, "title", None)
    if title is not None:
        print(title)
    elif not child.isspace():
        print(child)