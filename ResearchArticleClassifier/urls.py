"""
Created On: 20th Sept 2015
@author: Amitayush Thakur
"""
from django.views.generic.base import RedirectView

"""ResearchArticleClassifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
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
from django.conf.urls import include, url, patterns
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^myapp/',include('myapp.urls')),
    url(r'^uploadFile/$', RedirectView.as_view(url='/myapp/list/', permanent=True)),
]

urlpatterns += patterns('GUI.views',
    url(r'^home/$','loadHome'),
    url(r'^results/$','showResults'),
    url(r'^generateText/$','trainingDataList'),
    url(r'^addWordToDb/$','populateWordDb'),
    url(r'^KNN/$','applyKNN'),
    url(r'^Bayesian/$','callBayesian')
)

