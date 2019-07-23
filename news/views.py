from django.shortcuts import render
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup


def scrape():
    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
                                     'Safari/537.36'}
    url = 'https://www.theonion.com/'

    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, 'html.parser')

    columns = soup.find_all('div', {'class': 'curation-module__zone'}) # return a list
    print(len(columns))


scrape()