"""app_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^index/$', restIndexView , name='restIndex'),
    url(r'^woj/(?P<woj_id>[0-9]+)/$', restWojView , name='restWoj'),
    url(r'^pow/(?P<pow_id>[0-9]+)/$', restPowView, name='restPow'),
    url(r'^gmina/(?P<gmi_id>[0-9]+)/$', restGmiView, name='restGmi'),
    url(r'^obwod/(?P<obw_id>[0-9]+)/$', restObwView, name='restObw'),
]