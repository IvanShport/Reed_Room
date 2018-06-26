from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='chat'),
    url(r'^create_chat/$', views.CreateChatView, name='create_chat'),
    url(r'^(?P<pk>\d+)/$', views.OpenChatView, name='open_chat'),
    url(r'^(?P<pk>\d+)/send/$', views.SendMessageView, name='send'),
    url(r'^(?P<pk>\d+)/join/$', views.JoinView, name='join'),

]
