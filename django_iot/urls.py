"""Django for IoT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from apps.devices import views
from django.contrib.auth import views as auth_views
from apps.devices.forms import LoginForm

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^create/$', views.create, name='create'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html','authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name':'logout.html'}, name='logout'),
    url(r'^communicate/(?P<id>\d+)', views.communicate, name='communicate'),
    url(r'^communicate/(?P<room>\w+)$', views.group, name='group'),
    url(r'^control/', views.control, name='control'),
    url(r'^controlGroup/',views.controlGroup, name='controlGroup')
]
