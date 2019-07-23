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

    posts = soup.find_all('div', {'class': 'zone__item'})  # return a list

    for i in posts:
        link = i.find_all('section', {'class': 'content-meta__headline__wrapper'})[1]
        image_source = i.find('img', {'data-format': 'jpg'})['srcset']
    print(link.text)
    print((image_source))
scrape()
