from bs4 import BeautifulSoup
from django.shortcuts import redirect, render
import requests
from .models import Headline, UserProfile
from datetime import timezone, datetime
import os
import shutil

requests.packages.urllib3.disable_warnings()


def scrape(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    if user_p is not None:
        user_p.last_scrape = datetime.now(timezone.utc)
        user_p.save()

    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
                                     'Safari/537.36'}
    url = 'http://books.toscrape.com/'

    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, 'html.parser')

    posts = soup.find_all('article', {'class': 'product_pod'})  # return a list

    for i in posts:
        link = i.find('a', {'class': False, 'title': True})['href']
        title = i.find('img', {'class': 'thumbnail'})['alt']
        image_source = i.find('img', {'class': 'thumbnail'})['src']

        print(link)
        print(title)
        print(image_source)

        # stackoverflow solution

        media_root = 'C:/Users/Interbiz/PycharmProjects/media_root'
        if not image_source.startswith(("data:image", "javascript")):
            local_filename = image_source.split('/')[-1].split("?")[0]
            r = session.get(image_source, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)

        # end of stackoverflow solution

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = local_filename
        new_headline.save()

    return redirect('/')

