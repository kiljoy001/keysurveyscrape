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
#driver.implicitly_wait(2)
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
main = driver.find_element_by_xpath("//*[@id='main']")
main.click()

element = WebDriverWait(driver, 1).until(
EC.element_to_be_clickable((By.XPATH, "//*[@id='treeContainer']/ul/li[2]/ul//li")))
list = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul/li[2]/ul//li/a")

print(len(list))
for entry in list:
    element = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='treeContainer']/ul/li[2]/ul//li/a")))
    entry.click()
    newlist = entry.find_elements_by_xpath("//*[@id='treeContainer']/ul/li[2]/ul//li/ul//li//a")
bsObjList = []
for items in newlist:
    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='treeContainer']/ul/li[2]/ul//li/ul//li//a")))
    ActionChains(driver).move_to_element(items).click(items).perform()
    #html = urlopen(driver.current_url)
    bsObj = BeautifulSoup(driver.page_source, "html.parser")
    bsObjList.append(bsObj)
print("number of bsObjects: ", len(bsObjList))
for entry in bsObjList:
    print(entry.prettify())
#for items in list:
    #subList = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul/li[2]/ul//li/ul//li//ul//li")
    #print("sublist: ", len(subList))
    #print(items.get_attribute("data-rights"), items.get_attribute("title"), items.get_attribute("class"), items.get_attribute("id"))
    #for stuff in cycle(newlist):
        #if not stuff.get_attribute("class") == "last":
                #print(stuff.get_attribute("data-rights"), stuff.get_attribute("title"), stuff.get_attribute("id"))
        #else:
            #break

        #print(entry.get_attribute("title"), items.get_attribute("title"))
#//*[@id="treeContainer"]/ul/li[2]/ul
#release browser
#driver.close()

