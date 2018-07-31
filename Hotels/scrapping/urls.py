from django.conf.urls import url
from . import views

app_name = 'hotel_locations'

urlpatterns = [
    url(r'start/$', views.scrapping,name='scrapping')
]
