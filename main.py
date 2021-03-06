from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from db import mydb
import time
import re
import mysql.connector


CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('window-size=800x600')
chrome_options.add_argument('no-proxy-server')
chrome_options.add_argument("proxy-server='direct://'")
chrome_options.add_argument("proxy-bypass-list=*")
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome(executable_path='Chrome/chromedriver', options=chrome_options)  


def main(keyword):
    dictionary = {}
    go_to_google()
    slow_type(keyword)
    get_suggestions(dictionary)
    get_amount_of_searches(dictionary)
    insert_into_db(dictionary, keyword)
    driver.quit


def find_search_bar():
    try:
        search_field = driver.find_element_by_name("q")

    except EC.StaleElementReferenceException:
        search_field = driver.find_element_by_name("q")

    return search_field


def go_to_google():
    driver.get("http://www.google.com")
    try:
        driver.find_element_by_id('zV9nZe').click()
    except EC.NoSuchElementException:
        pass


def slow_type(keyword, delay=0.1):
    find_search_bar().send_keys(Keys.CONTROL + "a")
    find_search_bar().send_keys(Keys.DELETE)
    for character in keyword:
        find_search_bar().send_keys(character)
        time.sleep(delay)
    

def get_suggestions(dictionary):
    for item in driver.find_elements_by_css_selector('[role="listbox"] > li'):
        dictionary.setdefault('suggestion',[]).append(item.text)
    

def get_amount_of_searches(dictionary):
    for lst in dictionary.values():
        for item in lst:
            slow_type(item)
            find_search_bar().send_keys(Keys.ENTER)
            try:
                amount = driver.find_element_by_id('result-stats').text;
                amount = re.sub("[\(\[].*?[\)\]]", "", amount)
                amount = re.findall("\d+" , amount)
                amount = ' '.join([str(elem) for elem in amount])
                dictionary.setdefault('results',[]).append(amount)

            except EC.NoSuchElementException:
                driver.find_element_by_id("pnnext").click()
                amount = driver.find_element_by_id('result-stats').text;
                amount = re.sub("[\(\[].*?[\)\]]", "", amount)
                amount = re.findall("\d+" , amount)
                amount = ' '.join([str(elem) for elem in amount])
                dictionary.setdefault('results',[]).append(amount)
        return


def insert_into_db(dictionary, keyword):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS storage (id INT AUTO_INCREMENT PRIMARY KEY, suggestion VARCHAR(255), results VARCHAR(255), parent VARCHAR(255))")
    for lst in dictionary.values():
        for x in range(len(lst)):
            suggestion = [item for item in dictionary['suggestion']]
            result = [item for item in dictionary['results']]
            sql = ("INSERT INTO storage "
               "(suggestion, results, parent) "
               "VALUES (%s, %s, %s)")
            val = (suggestion[x], result[x], keyword)
            mycursor.execute(sql, val)
            mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        return 

