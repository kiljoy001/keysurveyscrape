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
driver.implicitly_wait(2)
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
#element = WebDriverWait(driver, 1).until(
#EC.element_to_be_clickable((By.XPATH, "//*[@id='main']")))
main = driver.find_element_by_css_selector("#main")
main.click()

list = driver.find_elements_by_css_selector("#treeContainer > ul > li.canNotCreate.open.notActiveNode > ul > *")

print("list of top level items: ",len(list))
topLevel ={}
for item in list:
    print("Top Level:", item.tag_name, item.text)
    topLevel[item.get_attribute("id")] = item.get_attribute("title")
    ActionChains(driver).move_to_element(item).click(item).perform()

closed = driver.find_elements_by_xpath("//*[@id='treeContainer']//a[contains(@class, 'close')]")
if len(closed) > 0:
    for each in closed:
        list.append(each)
    else:
        pass

for item in list:
    list2 = item.find_elements_by_css_selector("ul > *")
    for each in list2:
        print("List 2:", each.tag_name, each.text)
        ActionChains(driver).move_to_element(each).click(each).perform()
