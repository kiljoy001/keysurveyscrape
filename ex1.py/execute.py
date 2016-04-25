from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
#login to keysurvey
#driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver = webdriver.Chrome(executable_path=r'C:\phantomjs-2.1.1-windows\bin\chromedriver.exe')
driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
eleUsername = driver.find_element_by_id("login")
elePassword = driver.find_element_by_id("password")
eleUsername.send_keys("RTCResearch@rtc.edu")
elePassword.send_keys("R3search1")
driver.find_element_by_id("loginButton").click()
#https://app.keysurvey.com/app/action/Home/view/main/
#select reports link
checkUrl = driver.current_url
print(driver.current_url)
try:
    driver.execute_script("function login() {document.getElementByName('killConcurrentSessions').setAttribute('value','true');}")
    print("alert accepted")
except TimeoutException:
    print("No alert!")
print(driver.current_url)
#driver.find_element_by_xpath("//a[@title='Reports']").click()
#https://app.keysurvey.com/app/action/report/Home/view/custom/
#open main link
#print(driver.page_source)
driver.find_element_by_id("main").click()
allLinks = driver.find_elements_by_xpath("//a[@href='#']")
for items in allLinks:
    print ("Values are: {0}, {1}, {2}".format(items.get_attribute("class"), items.get_attribute("id"), items.get_attribute("title")))

driver.close()