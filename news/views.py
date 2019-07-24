from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()


def scrape():
    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
                                     'Safari/537.36'}
    url = 'http://books.toscrape.com/'

    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, 'html.parser')

    posts = soup.find_all('article', {'class': 'product_pod'})  # return a list

    for i in posts:
        link = i.find('a', {'class': False})['href']
        title = i.find('img', {'class': 'thumbnail'})['alt']
        image_source = i.find('img', {'class': 'thumbnail'})['src']
        print(link)
        print(title)
        print(image_source)


scrape()
