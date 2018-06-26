from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.LoginView, name='login'),
    url(r'^regist/$', views.RegistView, name='regist'),
    url(r'^logout/$', views.LogoutView, name='logout'),
]
