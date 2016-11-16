from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import time
import yaml
import os
import requests


def check_url(urlStore, WebDriver):
    """
    Compares input url to current url, splits url if there is a /? characters in it.
    :param urlStore:
    :return: boolean
    """
    currentURL = WebDriver.current_url
    substring = '/?'
    if substring in currentURL:
        processURL = currentURL.split('/?')
        if processURL[0] in urlStore:
            return True
        else:
            return False
    else:
        if currentURL == urlstore:
            return True
        else:
            return False


def execute_xpath(WebDriver, string):
    """
    Click on passed xpath element
    :param string: must be in XPath format
    :return: none
    """

    element = WebDriverWait(WebDriver, 5, .125).until(
        EC.element_to_be_clickable((By.XPATH, string)))
    element.click()
    return


def execute_css(WebDriver, string):
    """
    Click on passed xpath element
    :param string: must be in CSS format
    :return: none
    """

    element = WebDriverWait(WebDriver, 5, .125).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, string)))
    element.click()
    return


def check_for_record():
    """
    checks if there is a record file, if it exists load number into global accum variable
    :return:
    """
    global accum
    if accum is 1:
        if os.path.isfile('record.txt'):
            with open('record.txt', 'r') as number:
                accum = int(number.read())
                number.close()
            return accum
    else:
        pass


def record_place():
    """
    Records object number to record.txt, to be used on crashes for restarting the script as a place holder.
    :return:
    """
    global accum
    objnumber = accum
    if os.path.isfile('record.txt'):
        with open('record.txt', 'r+') as file:
            if int(file.read()) < int(accum):
                file.close()
                with open('record.txt', 'w+') as f:
                    f.write(str(objnumber))
                    f.close()
            else:
                print('Files downloaded are greater than the last attempt, record not saved.')
    else:
        with open('record.txt', 'w') as file:
            file.write(str(objnumber))
            file.close()


def check_jquery():
    """
    Check if jquery is active on page
    :return: boolean
    """
    check = WebDriverWait(driver, 30, .125).until(lambda s: s.execute_script("return jQuery.active == 0"))
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


def create_list(drFolder, drSurveys):
    """create clear and create list of folder items"""
    combined = []
    for stuff in drFolder:
        combined.append(stuff)
    for stuff2 in drSurveys:
        combined.append(stuff2)
    return combined


def get_report_number(urlstore):
    """rips report and survey number from url and returns it as substring"""
    if check_jquery():
        # splits the entire url into two chunks
        urlExtract = urlstore.split('/s')
        # splits the substring chunk (the second half of the original split) further with surveyID in position 0 and
        # report number in position 1
        substring = str(urlExtract[1]).split('/?rid=')
        return substring


def listAll(reportnum, surveynum, reportname, foldername):
    """Gets report name, folder name and saves it to a file"""
    if os.path.isfile('names.txt'):
        with open('names.txt', 'a+') as file:
            file.write("report:{0}, survey:{1}, report name:{2}, folder:{3},\n".format(reportnum, surveynum, reportname,
                                                                                       foldername))
            file.close()
    else:
        with open('names.txt', 'w') as createfile:
            createfile.write("report:{0}, survey:{1}, report name:{2}, folder:{3},\n".format(reportnum, surveynum,
                                                                                             reportname, foldername))
            createfile.close()


def pdf_json_check(report, survey):
    """
    :param report: report number of the download, accessible through the get_report_number function
    :param survey: survey number of the download, accessible through the get_report_number function
    :return: boolean that evaluates the json response as true or false
    """
    url = "https://app.keysurvey.com/app/public/export/evo/report/check/{0}/{1}?link=2?msigFromMain=1"
    response = requests.get(url.format(survey, report))
    data = response.json()
    if response.status_code is not 200:
        raise requests.ConnectionError()
    if type(data) is dict:
        msg_value = data.get('msg')
        if msg_value == 'progress':
            return False
        else:
            return True


def inner_loop():
    css_path = "#listContainer > ul > li:nth-child({0}) a"
    # nth-child cannot be zero, thus count starts at one and is extended by one to get the last element
    findSub = driver.find_elements_by_css_selector("#listContainer > ul a")
    subIndex = len(findSub)
    check_jquery()
    for unit in range(1, subIndex + 1):
        if check_jquery() and unit > 0:
            getname = driver.find_element_by_css_selector(css_path.format(unit)).text
            getfolder = driver.find_element_by_css_selector('#folderNameLabel').text
            driver.find_element_by_css_selector(css_path.format(unit)).click()
            reports = get_report_number(driver.current_url)
            listAll(reports[1], reports[0], getname, getfolder)
            # download loop for pdf
            if check_jquery():
                pdfClick = WebDriverWait(driver, 5, .125).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Print to PDF")))
                pdfClick.click()
                if check_jquery():
                    driver.find_element_by_id('printToPDF').click()
                    # explicit wait that checks if json returns anything other than 'progress' msg,
                    #  long wait time added to let the file download. Currently set to 5 minutes
                    WebDriverWait(driver, 300, 5).until(lambda check: pdf_json_check(reports[1], reports[0])
                       )
                    javaCheck = WebDriverWait(driver, 30, .125).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                    if javaCheck:
                        checkagain = WebDriverWait(driver, 30, .125).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                        if checkagain:
                            reportsLink = driver.find_element_by_xpath("//*[@id='emptySel']/a")
                            ActionChains(driver).move_to_element(reportsLink).click(
                                reportsLink).perform()
                            if check_url(urlstore, driver):
                                # download loop for csv
                                if check_jquery():
                                    csvClick = WebDriverWait(driver, 5, .125).until(
                                        EC.element_to_be_clickable((By.LINK_TEXT, "Export to CSV")))
                                    csvClick.click()
                                    if check_jquery():
                                        driver.execute_script("downloadExportWithLink(3,4);")
                                        javaCheck = WebDriverWait(driver, 30, .125).until(
                                            EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                                        if javaCheck:
                                            checkagain = WebDriverWait(driver, 30, .125).until(
                                                EC.element_to_be_clickable(
                                                    (By.XPATH, "//*[@id='emptySel']/a")))
                                            if checkagain:
                                                reportsLink = driver.find_element_by_xpath(
                                                    "//*[@id='emptySel']/a")
                                                ActionChains(driver).move_to_element(reportsLink).click(
                                                    reportsLink).perform()
                                                if check_url(urlstore, driver):
                                                    continue
                                                else:
                                                    time.sleep(10)  # delay for 10 seconds
                                                    if not check_url(urlstore, driver):
                                                        checklink = WebDriverWait(driver, 5, .125).until(
                                                            EC.element_to_be_clickable(
                                                                (By.XPATH, "//*[@id='emptySel']/a")))
                                                        if checklink and check_jquery():
                                                            ActionChains(driver).move_to_element(
                                                                checklink).click(
                                                                checklink).perform()
                                                    continue
                            else:
                                time.sleep(10)  # delay for 10 seconds
                                if not check_url(urlstore, driver):
                                    checklink = WebDriverWait(driver, 5, .125).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id='emptySel']/a")))
                                    if checklink and check_jquery():
                                        ActionChains(driver).move_to_element(checklink).click(
                                            checklink).perform()
                                        # download loop for csv
                                        if check_jquery():
                                            csvClick = WebDriverWait(driver, 5, .125).until(
                                                EC.element_to_be_clickable((By.LINK_TEXT, "Export to CSV")))
                                            csvClick.click()
                                            if check_jquery():
                                                driver.execute_script("downloadExportWithLink(3,4);")
                                                javaCheck = WebDriverWait(driver, 30, .125).until(
                                                    EC.element_to_be_clickable(
                                                        (By.XPATH, "//*[@id='emptySel']/a")))
                                                if javaCheck:
                                                    checkagain = WebDriverWait(driver, 30, .125).until(
                                                        EC.element_to_be_clickable(
                                                            (By.XPATH, "//*[@id='emptySel']/a")))
                                                    if checkagain:
                                                        reportsLink = driver.find_element_by_xpath(
                                                            "//*[@id='emptySel']/a")
                                                        ActionChains(driver).move_to_element(
                                                            reportsLink).click(
                                                            reportsLink).perform()
                                                        if check_url(urlstore, driver):
                                                            continue
                                                        else:
                                                            time.sleep(10)  # delay for 10 seconds
                                                            if not check_url(urlstore, driver):
                                                                checklink = WebDriverWait(driver, 5, .125).until(
                                                                    EC.element_to_be_clickable((By.XPATH,
                                                                                                "//*[@id='emptySel']/a")))
                                                                if checklink and check_jquery():
                                                                    ActionChains(driver).move_to_element(
                                                                        checklink).click(
                                                                        checklink).perform()
                                                            continue


def configFile():
    """loads configuration yaml info from a yaml file Must specify path to file in raw text.
        :return dictionary
    """
    # location of the .yaml file changes with the folder position
    with open(r'config.yaml') as f:
        return yaml.load(f)


config = configFile()
chrome_path = Options()
chrome_path.binary_location = config['driverpath']
# alert_handling = webdriver.DesiredCapabilities.CHROME.copy()
# alert_handling['unexpectedAlertBehaviour'] = "accept"
driver = webdriver.Chrome(executable_path=config['altdriver'], chrome_options=chrome_path)
driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
eleUsername = driver.find_element_by_id("login")
elePassword = driver.find_element_by_id("password")

eleUsername.send_keys(config['login'])
elePassword.send_keys(config['password'])

driver.find_element_by_id("loginButton").click()

driver.maximize_window()
driver.find_element_by_xpath("//a[@href='/Member/ReportWizard/dashboard.do ']").click()
execute_xpath(driver, "//*[@id='main']")
accum = 1
check_for_record()
loop = True
global elecontainer
try:
    while loop:
        open_folders()
        # elecontainer = create_list(lambda: driver.find_elements_by_xpath("//*[@data-rights='16711680']"), lambda: driver.find_elements_by_xpath("//*[data-rights='16777215']"))
        elecontainer = driver.find_elements_by_css_selector("a[data-rights^='167']")
        map(lambda: driver.find_elements_by_css_selector("a[data-rights^='167']"), elecontainer)
        if elecontainer[accum].is_displayed():
            ActionChains(driver).move_to_element(elecontainer[accum]).click(elecontainer[accum]).perform()
            if check_jquery():
                urlstore = driver.current_url
                inner_loop()
        accum += 1
except StaleElementReferenceException as stale:
    record_place()
    print(stale)
    print("accum is: " + accum)
    print("length of list is ", len(elecontainer))
except Exception as e:
    record_place()
    print(e)
    print("accum is: " + str(accum))
    print("length of list is ", len(elecontainer))
