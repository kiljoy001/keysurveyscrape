from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import deque
from selenium.webdriver.common.action_chains import ActionChains
import itertools


def execute_xpath(WebDriver, string):
    """
    Click on passed xpath element
    :param string: must be in XPath format
    :return: none
    """

    element = WebDriverWait(WebDriver, 5).until(
        EC.element_to_be_clickable((By.XPATH, string)))
    element.click()
    return


def execute_css(WebDriver, string):
    """
    Click on passed xpath element
    :param string: must be in XPath format
    :return: none
    """

    element = WebDriverWait(WebDriver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, string)))
    element.click()
    return


def check_jquery():
    """
    Check if jquery is active on page
    :return: boolean
    """
    check = WebDriverWait(driver, 20).until(lambda s: s.execute_script("return jQuery.active == 0"))
    if check:
        result = True
    else:
        result = False
    return result


def open_folders():
    """crawls through keysurvey folder list and opens all folders"""
    check_jquery()
    if check_jquery():
        folderTree = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul//ul//a")
    check_jquery()
    if check_jquery():
        for unit in range(len(folderTree)):
            check_jquery()
            if check_jquery():
                if folderTree[unit].is_displayed() and folderTree[unit].get_attribute("class") == "surveyFolderOpen":
                    continue
                else:
                    ActionChains(driver).move_to_element(folderTree[unit]).click(folderTree[unit]).perform()
        test = driver.find_elements_by_xpath("//*[@data-rights='16777215']")
        test2 = driver.find_elements_by_xpath("//*[@data-rights='16711680']")
        for each in range(len(test)):
            check_jquery()
            if check_jquery():
                if test[each].is_displayed() and test[each].get_attribute("class") == "surveyFolderOpen":
                    continue
                else:
                    ActionChains(driver).move_to_element(test[each]).click(test[each]).perform()
        combined = []
        for stuff in test:
            combined.append(stuff)
        for stuff2 in test2:
            combined.append(stuff2)
        for each2 in range(len(combined)):
            check_jquery()
            if check_jquery():
                if combined[each2].is_displayed() and combined[each2].get_attribute("class") == "surveyFolderOpen":
                    continue
                else:
                    ActionChains(driver).move_to_element(combined[each2]).click(combined[each2]).perform()


def inner_loop(combined):
    css_path = "#listContainer > ul > li:nth-child({0}) a"
    outerlist = deque(combined)
    try:
        for item in range(len(outerlist)):
            if outerlist[item].is_displayed() and outerlist[item].get_attribute("class") == "surveyFolderOpen":
                ActionChains(driver).move_to_element(outerlist[item]).click(outerlist[item]).perform()
    # nth-child cannot be zero, thus count starts at one and is extended by one to get the last element

        findSub = driver.find_elements_by_css_selector("#listContainer > ul a")
        subIndex = len(findSub)
        for unit in range(1, subIndex + 1):
            if check_jquery() and unit > 0:
                driver.find_element_by_css_selector(css_path.format(unit)).click()
                # download loop
                if check_jquery():
                    csvClick = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Export to CSV")))
                    csvClick.click()
                    if check_jquery():
                        driver.execute_script("downloadExportWithLink(3,4);")
                        javaCheck = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                        if javaCheck:
                            checkagain = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                            if checkagain:
                                reportsLink = driver.find_element_by_xpath("//*[@id='emptySel']/a")
                                ActionChains(driver).move_to_element(reportsLink).click(
                                    reportsLink).perform()

    except NoSuchElementException:
        pass
    except StaleElementReferenceException:
        pass




driver = webdriver.Chrome(executable_path=r'C:\ProgramData\chocolatey\lib\chromedriver\tools\chromedriver.exe')
driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
eleUsername = driver.find_element_by_id("login")
elePassword = driver.find_element_by_id("password")
eleUsername.send_keys("RTCResearch@rtc.edu")
elePassword.send_keys("R3search1")
# eleUsername.send_keys("kiljoy001@gmail.com")
# elePassword.send_keys("$Master001")
driver.find_element_by_id("loginButton").click()

driver.maximize_window()
driver.find_element_by_xpath("//a[@href='/Member/ReportWizard/dashboard.do ']").click()
execute_xpath(driver, "//*[@id='main']")

try:
    list = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul//ul//a")
    open_folders()

except StaleElementReferenceException:
    open_folders()

