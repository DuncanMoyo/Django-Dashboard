from django.conf.urls import url
from .views import create_view

app_name = "notepad"

urlpatterns = [
    url(r'^create/', create_view, name='create')
]