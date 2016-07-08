from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
from selenium.webdriver.common.action_chains import ActionChains
import itertools



def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def get_element(node):
    # for XPATH we have to count only for nodes with same type!
    length = len(list(node.previous_siblings)) + 1
    if length > 1:
        return '%s:nth-child(%s)' % (node.name, length)
    else:
        return node.name


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


def nested_dict_iter(nested):
    for key, value in nested.iteritems():
        if isinstance(value, collections.Mapping):
            for inner_key, inner_value in nested_dict_iter(value):
                yield inner_key, inner_value
        else:
            yield key, value


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

# login to keysurvey

driver = webdriver.Chrome(executable_path=r'C:\ProgramData\chocolatey\lib\chromedriver\tools\chromedriver.exe')

driver.get('https://app.keysurvey.com/Member/UserAccount/UserLogin.action')
eleUsername = driver.find_element_by_id("login")
elePassword = driver.find_element_by_id("password")
eleUsername.send_keys("RTCResearch@rtc.edu")
elePassword.send_keys("R3search1")
# eleUsername.send_keys("kiljoy001@gmail.com")
# elePassword.send_keys("$Master001")
driver.find_element_by_id("loginButton").click()
# https://app.keysurvey.com/app/action/Home/view/main/
# select reports link
driver.maximize_window()
driver.find_element_by_xpath("//a[@href='/Member/ReportWizard/dashboard.do ']").click()
execute_xpath(driver, "//*[@id='main']")
try:
    accum = 0

    if check_jquery():
        # endPoints = driver.find_elements_by_xpath("//li[starts-with(@id, 's')]")
        folderTree = driver.find_elements_by_css_selector(".close > a")
        loop = True
        while loop:
            if not folderTree:
                loop = False
            for element in folderTree:
                if accum > 0:
                    # move to the next element
                    check_jquery()
                    if check_jquery():
                        ActionChains(driver).move_to_element(folderTree[accum]).click(folderTree[accum]).perform()
                        if accum == len(folderTree):
                            endPoints = "#treeContainer > ul > li:nth-child({0}) > ul  li:nth-child(2) > ul a"
                            for num in range(1, len(folderTree) + 1):
                                driver.find_element_by_css_selector(endPoints.format(num)).click()

                    check_jquery()
                    # cycle through the middle section of the page
                    if check_jquery():
                        subIndex = len(driver.find_elements_by_css_selector("#listContainer > ul a"))
                        endPoint = "#treeContainer > ul > li > ul  li:nth-child({0}) > ul a"
                        css_path = "#listContainer > ul > li:nth-child({0}) a"
                    # nth-child cannot be zero, thus count starts at one and is extended by one to get the last element
                        if not subIndex:
                            accum += 1
                            continue
                        else:
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

                    folderTree.clear()
                    folderTree = driver.find_elements_by_css_selector(".close > a")
                    if len(folderTree) <= accum:
                        accum += 1
                    else:
                        continue
                else:
                    check_jquery()
                    if check_jquery():
                        ActionChains(driver).move_to_element(folderTree[accum]).click(folderTree[accum]).perform()
                        endPoints = element.find_elements_by_css_selector("ul > *")
                        check_jquery()
                        if check_jquery():
                            subIndex = len(driver.find_elements_by_css_selector("#listContainer > ul a"))
                            css_path = "#listContainer > ul > li:nth-child({0}) a"
                            if not subIndex:
                                accum += 1
                                continue
                            else:
    # nth-child cannot be zero, thus count starts at one and is extended by one to get the last element
                                for unit in range(1, subIndex + 1):
                                    if check_jquery() and unit >= 0:
                                        driver.find_element_by_css_selector(css_path.format(unit)).click()
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
                                                        reportsLink = driver.find_element_by_xpath(
                                                            "//*[@id='emptySel']/a")
                                                        ActionChains(driver).move_to_element(reportsLink).click(
                                                            reportsLink).perform()



                    accum += 1
                    folderTree.clear()
                    folderTree = driver.find_elements_by_css_selector(".close > a")

        if accum > len(folderTree):
            loop = False

except NoSuchElementException as ns:
    print("Error! {0}".format(ns))

except StaleElementReferenceException as se:
    print("Error! {0}".format(se))


