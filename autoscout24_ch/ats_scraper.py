
import json
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

SET_NAME = 'autoscout24_ch'
URL = 'https://www.autoscout24.ch/de/'
MAKES_CONTAINER_ID = 'make'
MODELS_CONTAINER_ID = 'model'

def scraper():
    page = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    with open('makes.json', 'w') as makes_file:
        data = {}
        data[SET_NAME] = []
        for option in soup.find(id = MAKES_CONTAINER_ID):
            if option['value'] == '' or option['value'] < str(0):
                continue
            make = {}
            make['i'] = option['value']
            make['n'] = option.get_text().lower()
            data[SET_NAME].append(make)
            
        for make in data[SET_NAME]:
            page = requests.get(URL + '?make=' + str(make['i']), headers = HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')

            make['models'] = []
            for option in soup.find(id = MODELS_CONTAINER_ID):
                if option['value'] == '' or option['value'] < str(0):
                    continue
                model = {}
                model['v'] = option['value']
                model['m'] = option.get_text().lower().replace('\u00e9', '').replace('\u00a0', '')
                make['models'].append(model)

        json.dump(data, makes_file)
        makes_file.close()