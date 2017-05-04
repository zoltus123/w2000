"""w2000 URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app_wybory.views import index, wojNazView, wojewodztwoView, powiatView, gminaView, obwodView
from django.conf import settings
from django.conf.urls.static import static

from app_wybory.views import loginView, logoutView, edytujView, szukajView

WOJEWODZTWA = "Dolnośląskie|Kujawsko-Pomorskie|Lubelskie|Lubuskie|Łódzkie|Małopolskie|Mazowieckie|Opolskie|Podkarpackie|Podlaskie|Pomorskie|Śląskie|Świętokrzyskie|Warmińsko-Mazurskie|Wielkopolskie|Zachodniopomorskie"

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^wyniki/woj/(?P<woj>' + WOJEWODZTWA + ')/$', wojNazView),
    url(r'^wyniki/woj/(?P<woj_id>[0-9]+)/$', wojewodztwoView, name='wojewodztwo'),
    url(r'^wyniki/pow/(?P<pow_id>[0-9]+)/$', powiatView, name='powiat'),
    url(r'^wyniki/gmina/(?P<gmi_id>[0-9]+)/$', gminaView, name='gmina'),
    url(r'^wyniki/obwod/(?P<obw_id>[0-9]+)$', obwodView, name='obwod'),
    url(r'^szukaj/$', szukajView, name='szukaj'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', loginView, name='login'),
    url(r'^logout/', logoutView, name='logout'),
    url(r'^szukaj/', szukajView),
    url(r'^edytuj/(?P<obw_id>[0-9]+)/(?P<kand_id>[0-9]+)', edytujView, name='edytuj')
]
