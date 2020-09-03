
import json, time, requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

SET_NAME = 'anibis_ch'
URL = 'https://www.anibis.ch/fr/c/automobiles-voitures-de-tourisme'

def scrape_makes():

    try:
        with open('makes.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    page = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    with open('makes.json', 'w') as json_file:
        data[SET_NAME] = []
        for option in soup.find_all('select')[2]:
            if option['value'] == '' or option['value'] < str(0):
                continue
            make = {}
            make['i'] = option['value']
            make['n'] = option.get_text().lower()
            data[SET_NAME].append(make)

        json.dump(data, json_file)
