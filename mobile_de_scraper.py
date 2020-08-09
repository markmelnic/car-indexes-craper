
import json
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

SET_NAME = 'mobile_de'
URL = 'https://www.mobile.de/?vc=Car'
MAKES_CONTAINER_ID = 'qsmakeBuy'
MODELS_CONTAINER_ID = 'qsmodelBuy'

def scrape_makes():
    
    try:
        with open('makes.json') as json_file:
            data = json.load(json_file)
            json_file.close
    except FileNotFoundError:
        data = {}

    page = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    with open('makes.json', 'w') as json_file:
        data[SET_NAME] = []
        for option in soup.find(id = MAKES_CONTAINER_ID):
            if option['value'] == '' or option['value'] < str(0):
                continue
            make = {}
            make['i'] = option['value']
            make['n'] = option.get_text().lower()
            data[SET_NAME].append(make)

        json.dump(data, json_file)
        json_file.close()


def scrape_models():
    
    with open('makes.json') as json_file:
            data = json.load(json_file)
            json_file.close

    with open('makes.json', 'w') as json_file:
        for make in data[SET_NAME]:
            page = requests.get(URL + '&mk=' + str(make['i']), headers = HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')

            make['models'] = []
            for option in soup.find(id = MODELS_CONTAINER_ID):
                if option['value'] == '' or option['value'] < str(0):
                    continue
                model = {}
                model['v'] = option['value']
                model['m'] = option.get_text().lower().replace('\u00e9', '').replace('\u00a0', '')
                make['models'].append(model)

        json.dump(data, json_file)
        json_file.close()
