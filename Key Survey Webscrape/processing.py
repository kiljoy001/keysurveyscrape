import os
import re
import index
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


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

        def open_folders():
            """crawls through folder list, returns list of folders crawled in a list"""
            grab_text = []
            index.check_jquery()
            if index.check_jquery():
                folderTree = driver.find_elements_by_xpath("//*[@id='treeContainer']/ul//ul//a")
                index.check_jquery()
            if index.check_jquery():
                for unit in range(len(folderTree)):
                    index.check_jquery()
                    if index.check_jquery():
                        if folderTree[unit].is_displayed() and folderTree[unit].get_attribute(
                                "class") == "surveyFolderOpen":
                            continue
                        else:
                            ActionChains(driver).move_to_element(folderTree[unit]).click(folderTree[unit]).perform()
                            grab_text.append(folderTree[unit].text)
                folders = driver.find_elements_by_css_selector("a[data-rights^='167']")
                for each2 in range(len(folders)):
                    index.check_jquery()
                    if index.check_jquery():
                        if folders[each2].is_displayed() and folders[each2].get_attribute(
                                "class") == "surveyFolderOpen":
                            continue
                        else:
                            ActionChains(driver).move_to_element(folders[each2]).click(folders[each2]).perform()
                            grab_text.append(folders[each2].text)
            return grab_text


get_unique_surveys()
config = index.configFile()
chrome_path = index.Options()
chrome_path.binary_location = config['driverpath']
driver = webdriver.Chrome(executable_path=config['altdriver'], chrome_options=chrome_path)