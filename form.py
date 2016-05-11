from sys import argv
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def schedulePDF(self):
    self.driver = webdriver.Chrome(executable_path=r'E:\Projects\chromedriver.exe')
    self.driver.find_element_by_id("publishButtonD")