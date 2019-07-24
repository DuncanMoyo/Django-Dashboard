from django.contrib import admin
from django.conf.urls import url, include
from news.views import scrape, news_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^notes/', include('notepad.urls', namespace='notes')),
    url(r'^scrape', scrape, name='scrape'),
    url(r'^home', news_list, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)