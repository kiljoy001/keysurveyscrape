from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
xpath_soup = __import__(xpath_soup)
#login to keysurvey
#driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver = webdriver.Chrome(executable_path=r'C:\phantomjs-2.1.1-windows\bin\chromedriver.exe')
#driver = webdriver.Chrome(executable_path=r'E:\Projects\chromedriver.exe')
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
bsObj = BeautifulSoup(driver.page_source, 'html.parser')
mainXP = xpath_soup(bsObj.find(id="main"))