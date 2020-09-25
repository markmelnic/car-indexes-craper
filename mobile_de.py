
import json, time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SET_NAME = 'mobile_de'
URL = 'https://www.mobile.de/?vc=Car'
MAKES_CONTAINER_ID = 'qsmakeBuy'
MODELS_CONTAINER_ID = 'qsmodelBuy'

def scrape_makes():

    chrome_options = webdriver.ChromeOptions()
    dv = webdriver.Chrome(executable_path = "chromedriver.exe")

    try:
        with open('makes.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    dv.get(URL)
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(1)
    with open('makes.json', 'w') as json_file:
        data[SET_NAME] = []
        options = dv.find_element_by_id(MAKES_CONTAINER_ID).find_elements_by_tag_name('option')
        for option in options:
            if option.get_attribute('class') == 'pmak':
                continue
            if option.get_attribute('value') == '' or option.get_attribute('value') < str(0):
                continue
            make = {}
            make['i'] = option.get_attribute('value')
            make['n'] = option.text.lower()
            data[SET_NAME].append(make)

        json.dump(data, json_file)

    dv.quit()


def scrape_models():

    with open('makes.json') as json_file:
            data = json.load(json_file)

    chrome_options = webdriver.ChromeOptions()
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = "chromedriver.exe")

    with open('makes.json', 'w') as json_file:
        for make in data[SET_NAME]:
            dv.get(URL + '&mk=' + str(make['i']))
            WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
            time.sleep(1)
            make['models'] = []
            options = dv.find_element_by_id(MODELS_CONTAINER_ID).find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == '' or option.get_attribute('value') < str(0):
                    continue
                model = {}
                model['v'] = option.get_attribute('value')
                model['m'] = option.text.lower().replace('\u00e9', '').replace('\u00a0', '')
                make['models'].append(model)

            if make['models'] == []:
                options = dv.find_element_by_id(MODELS_CONTAINER_ID).find_elements_by_tag_name('option')
                for option in options:
                    if option.get_attribute('value') == '':
                        continue
                    model = {}
                    model['v'] = option.get_attribute('value')
                    model['m'] = option.text.lower().replace('\u00e9', '').replace('\u00a0', '')
                    make['models'].append(model)

        json.dump(data, json_file)

    dv.quit()
