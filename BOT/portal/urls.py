from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.Entry_Page, name='Entry_Page'),
    path('Chatbot_Page', views.Chatbot_Page,  name='Chatbot_Page'),
]
