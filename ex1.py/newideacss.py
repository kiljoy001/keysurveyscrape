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
#login to keysurvey
#driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
#driver = webdriver.Chrome(executable_path=r'C:\phantomjs-2.1.1-windows\bin\chromedriver.exe')
driver = webdriver.Chrome(executable_path=r'E:\Projects\chromedriver.exe')
driver.implicitly_wait(10)
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
#open main link

main = driver.find_element_by_css_selector("#main")
main.click()

list = driver.find_elements_by_css_selector("#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > *")

print("list of top level items: ",len(list))
topLevel ={}
#counter keeps track of the folder
counter = 0
for item in list:
    counter+=1
    print("Top Level:", counter, item.text)
    topLevel[item.get_attribute("id")] = item.get_attribute("title")
    ActionChains(driver).move_to_element(item).click(item).perform()

#keeps track of the subfolder
subCounter = 0
subLevel ={}
for item in list:
    #folder match - if the counter is the same then then subitems are in the same folder
    subCounter +=1
    list2 = item.find_elements_by_css_selector("ul > *")
    subLevel[item.get_attribute("id")] = item.get_attribute("title")
    for each in list2:
        print("List 2:", subCounter, each.text)
        ActionChains(driver).move_to_element(each).click(each).perform()
        list3 = driver.find_elements_by_css_selector(".aBodySList > ul > *")
        print("list3 len:", len(list3))
for entry in list3:
            ActionChains(entry).move_to_element(entry).click(entry).perform()
            exportLink = entry.find_element_by_css_selector("#exportCSVLink")
            ActionChains(exportLink).move_to_element(exportLink).click(exportLink).perform()
            selectLabelValue = entry.find_element_by_css_selector("#exportValuesLabelsCSV3")
            ActionChains(selectLabelValue).move_to_element(selectLabelValue).click(selectLabelValue).perform()
            btnScheduleReport = entry.find_element_by_css_selector("#FTPDIV > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > a")
            ActionChains(btnScheduleReport).move_to_element(btnScheduleReport).click(btnScheduleReport).perform()
            csvSelect = entry.find_element_by_css_selector("#exportTypeCSV")

#formatSettings > div > ul
#formatSettings > div > ul
#closed = driver.find_elements_by_xpath("//*[@id='treeContainer']//li[@class='close']")
#if len(closed) > 0:
    #for each in closed:
        #if each.text ==
        #list.append(each)
        #print("added to list!")
    #else:
        #pass

