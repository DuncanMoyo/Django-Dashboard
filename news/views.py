from django.shortcuts import render, redirect
import requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
import os
import shutil
from .models import Headline, UserProfile
import math

requests.packages.urllib3.disable_warnings()


def news_list(request):
    # user can only scrape once every 24 hours
    user_p = UserProfile.objects.filter(user=request.user).first()
    now = datetime.now(timezone.utc)
    time_difference = now - user_p.last_scrape
    time_difference_in_hours = time_difference / timedelta(minutes=60)
    next_scrape = 24 - time_difference_in_hours
    if time_difference_in_hours <= 24:
        hide_me = True
    else:
        hide_me = False

    headlines = Headline.objects.all()
    context = {
        'object_list': headlines,
        'hide_me': hide_me,
        'next_scrape': math.ceil(next_scrape)
    }
    return render(request, 'home.html', context)


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
        link = i.find('a', {'class': False})['href']
        title = i.find('img', {'class': 'thumbnail'})['alt']
        image_source = i.find('img', {'class': 'thumbnail'})['src']

        '''
        ================
        This code that has been commented is not working
        will need to find another way to collect ever-changing images
        ================
        
        '''

        # stackoverflow solution

#        if not image_source.startswith(("data:image", "javascript")):
 #           media_root = r"C:\Users\Interbiz\PycharmProjects\dashboard\media_root"
  #          local_filename = image_source.split('/')[-1].split("?")[0]
   #         r = session.get(image_source, stream=True, verify=False)

  #           with open(local_filename, 'wb') as f:
    #           for chunk in r.iter_content(chunk_size=1024):
      #              f.write(chunk)

       #  current_image_absolute_path = os.path.abspath(local_filename)
    #           for chunk in r.iter_content(chunk_size=1024):
      #              f.write(chunk)

#        shutil.move(current_image_absolute_path, media_root)

        # end of stackoverflow solution

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_source
        new_headline.save()

    return redirect('/')

