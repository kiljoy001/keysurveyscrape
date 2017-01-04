import os
import re
from selenium.webdriver.chrome.options import Options
import yaml
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
                search = re.findall('report:\d\d\d\d\d\d, each', text)
                surveydictionary[each] = surveyno.count(each), search
        # write out results with key value pairs representing the survey and how many times it shows up in the list
        file.close()
        fileout = open('surveys.txt', 'w')
        for k, v in surveydictionary.items():
            fileout.write('{0} number:{1}\n'.format(k, v))
        fileout.close()
# def csv_reader():
#     """takes path as string and opens all *.csv files
#     :return: output to text file
#     """
#     download_files = os.listdir(os.path.expanduser('~/Downloads'))


# get_unique_surveys()
compile_surveys()
# config = configFile()
# chrome_path = Options()
# chrome_path.binary_location = config['driverpath']
# driver = webdriver.Chrome(executable_path=config['altdriver'], chrome_options=chrome_path)
# driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
# eleUsername = driver.find_element_by_id("login")
# elePassword = driver.find_element_by_id("password")
# eleUsername.send_keys(config['login'])
# elePassword.send_keys(config['password'])
# driver.find_element_by_id("loginButton").click()
# driver.maximize_window()
# driver.find_element_by_xpath("//a[@href='/Member/ReportWizard/dashboard.do ']").click()
# execute_xpath(driver, "//*[@id='main']")
