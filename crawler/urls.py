# coding: utf-8

from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.toutiao),
    url(r'^mem$', views.sett),
]
