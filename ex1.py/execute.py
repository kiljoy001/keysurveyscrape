from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
#login to keysurvey
#driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver = webdriver.Chrome(executable_path=r'C:\phantomjs-2.1.1-windows\bin\chromedriver.exe')
#driver = webdriver.Chrome(executable_path=r'E:\Projects\chromedriver.exe')
driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
eleUsername = driver.find_element_by_id("login")
elePassword = driver.find_element_by_id("password")
eleUsername.send_keys("RTCResearch@rtc.edu")
elePassword.send_keys("R3search1")
driver.find_element_by_id("loginButton").click()
#https://app.keysurvey.com/app/action/Home/view/main/
#select reports link
driver.find_element_by_xpath("//a[@href='/Member/ReportWizard/dashboard.do ']").click()
print(driver.current_url)
#https://app.keysurvey.com/app/action/report/Home/view/custom/
#open main link
element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH, "//*[@id='main']")))
main = driver.find_element_by_xpath("//*[@id='main']")
main.click()

element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH, "//*[@id='treeContainer']/ul/li[2]/ul//li")))
list = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul/li[2]/ul//li/a")


print(len(list), )
for entry in list:
    print(entry.get_attribute("title"))
    entry.click()
    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='treeContainer']/ul/li[2]/ul//li//ul//li")))
    list = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul/li[2]/ul//li//ul//li")

   #if entry.get_attribute("class") == "canNotCreate open notActiveNode":
       #entry.find_elements_by_xpath("//li/a/")
#release browser
#driver.close()

