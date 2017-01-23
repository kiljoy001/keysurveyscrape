import os
import re
from selenium.webdriver.chrome.options import Options
import yaml
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


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

def get_list():
    if os.path.isfile('names.txt'):
        with open('names.txt', 'r+') as file:
            text = file.read()
            splitedtext =text.split('\n')
            filtered = set(splitedtext)
            file.close()
        fileout = open('filterednames.txt', 'w')
        for item in filtered:
            fileout.write('%s\n' % item)
        fileout.close()


def get_unique_surveys():
    if os.path.isfile('filterednames.txt'):
        # processing file to get the unique survey numbers
        with open('filterednames.txt', 'r+') as file:
            text = file.read()
            surveylist = []
            surveydictionary = {}
            surveyno = re.findall('survey:\d\d\d\d\d\d', text)
            surveylist.append(surveyno)

            get_unique = set(surveyno)
            for each in get_unique:
                surveydictionary[each] = surveyno.count(each)
                # write out results with key value pairs representing the survey and how many times it shows up in the list
        file.close()
        fileout = open('surveys.txt', 'w')
        for k, v in surveydictionary.items():
            fileout.write('{0} number:{1}\n'.format(k, v))
        fileout.close()


def configFile():
    """loads configuration yaml info from a yaml file Must specify path to file in raw text.
                :return dictionary
            """
    # location of the .yaml file changes with the folder position
    with open(r'config.yaml') as f:
        return yaml.load(f)

def record_folders():
    """crawls through folder list, returns list of folders crawled in a list"""
    # temp storage
    grab_text = []
    # crawl through
    check_jquery()
    if check_jquery():
        folderTree = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul//ul//a")
        check_jquery()
    if check_jquery():
        for unit in range(len(folderTree)):
            check_jquery()
            if check_jquery():
                if folderTree[unit].is_displayed() and folderTree[unit].get_attribute(
                        "class") == "surveyFolderOpen":
                    continue
                else:
                    ActionChains(driver).move_to_element(folderTree[unit]).click(folderTree[unit]).perform()
                    grab_text.append(folderTree[unit].text)
        folders = driver.find_elements_by_css_selector("a[data-rights^='167']")
        for each2 in range(len(folders)):
            check_jquery()
            if check_jquery():
                if folders[each2].is_displayed() and folders[each2].get_attribute(
                        "class") == "surveyFolderOpen":
                    continue
                else:
                    ActionChains(driver).move_to_element(folders[each2]).click(folders[each2]).perform()
                    grab_text.append(folders[each2].text)
    # write out to file
    with open('folderlist.txt', 'w') as file:
        for each in grab_text:
            file.write('{0}\n'.format(each))
        file.close()


def check_downloaded_pdf(list):
    download_files = os.listdir(os.path.expanduser('~/Downloads'))
    temp =[]
    for each in download_files:
        if each == re.findall('\*.pdf', each):
            temp.append(temp)
    result = [i for i, j in zip(temp, list) if temp == list]
    return result


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

def compile_surveys():
    if os.path.isfile('filterednames.txt'):
        # processing file to get the unique survey numbers
        with open('filterednames.txt', 'r+') as file:
            text = file.read()
            surveylist = []

            surveydictionary = {}
            surveyno = re.findall('survey:\d\d\d\d\d\d', text)
            surveylist.append(surveyno)

            get_unique = set(surveyno)
            for each in get_unique:
                search = re.findall('report:\d\d\d\d\d\d, {0}'.format(each), text) or re.findall('report:-1, {0}'.format(each), text)
                result = []
                for found in search:
                    cleanup = re.findall('report:\d\d\d\d\d\d', found) or re.findall('report:-1', found)
                    result.append(cleanup[0][7:])
                surveydictionary[each] = surveyno.count(each), result
        # write out results with key value pairs representing the survey and how many times it shows up in the list
        file.close()
        fileout = open('surveys.txt', 'w')
        for k, v in surveydictionary.items():
            fileout.write('{0} :: {1}\n'.format(k, v))
        fileout.close()


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


def gather_info():
    css_path = "#listContainer > ul > li:nth-child({0}) a"
    # nth-child cannot be zero, thus count starts at one and is extended by one to get the last element
    findSub = driver.find_elements_by_css_selector("#listContainer > ul a")
    subIndex = len(findSub)
    check_jquery()
    temp_storage = {}
    for unit in range(1, subIndex + 1):
            if check_jquery() and unit > 0:
                getname = driver.find_element_by_css_selector(css_path.format(unit)).text
                try:
                    getreport = driver.find_element_by_css_selector('.pre #reportNameText').text
                except NoSuchElementException:
                    getreport = driver.find_element_by_css_selector('#infoContainer .pre div').text
                get_survey_number = driver.find_element_by_xpath("//*[@id='infoContainer']/div[1]").text
                try:
                    get_report_number = driver.find_element_by_xpath("//*[@id='infoContainer']/div[2]").text
                except NoSuchElementException:
                    get_report_number = '-1'
                    if get_report_number is not '-1':
                        temp_storage["{0}_{1}".format(get_report_number[11:], get_survey_number[11:])] = getreport
                    else:
                        temp_storage["{0}_{1}".format(get_report_number, get_survey_number[11:])] = getreport
                driver.find_element_by_css_selector(css_path.format(unit)).click()
    if os.path.isfile('listed_files.txt'):
        with open('listed_files.txt','a+') as file:
            for k, v in temp_storage.items():
                file.write("{0}:{1}\n".format(k, v))
            file.close()
    else:
        with open('listed_files.txt', 'a+') as file:
            for k, v in temp_storage.items():
                file.write("{0}:{1}\n".format(k, v))
            file.close()



# def csv_reader():
#     """takes path as string and opens all *.csv files
#     :return: output to text file
#     """
#     download_files = os.listdir(os.path.expanduser('~/Downloads'))


# get_unique_surveys()
# compile_surveys()
config = configFile()
chrome_path = Options()
chrome_path.binary_location = config['driverpath']
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
record_folders()
accum = 1
check_for_record()
loop = True
global elecontainer
try:
    while loop:
        open_folders()
        elecontainer = driver.find_elements_by_css_selector("a[data-rights^='167']")
        map(lambda: driver.find_elements_by_css_selector("a[data-rights^='167']"), elecontainer)
        if elecontainer[accum].is_displayed():
            ActionChains(driver).move_to_element(elecontainer[accum]).click(elecontainer[accum]).perform()
            if check_jquery():
                urlstore = driver.current_url
                gather_info()
        accum += 1
except Exception as e:
    record_place()
    print("accum is: " + str(accum))
    print("length of list is ", len(elecontainer))