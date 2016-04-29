from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
#login to keysurvey
#driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
#driver = webdriver.Chrome(executable_path=r'C:\phantomjs-2.1.1-windows\bin\chromedriver.exe')
driver = webdriver.Chrome(executable_path=r'E:\Projects\chromedriver.exe')
driver.implicitly_wait(15)
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
    #WebDriverWait(driver, 120)
    entry.click()
    #WebDriverWait(driver, 120)
    newlist = entry.find_elements_by_class_name("surveyFolder")
    print(len(newlist))
    for items in newlist:
        if len(newlist) > 0:
            #WebDriverWait(driver, 360)
            items.click()
            #WebDriverWait(driver, 360)

        #print(entry.get_attribute("title"), items.get_attribute("title"))
#//*[@id="treeContainer"]/ul/li[2]/ul
#release browser
#driver.close()

