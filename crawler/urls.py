# coding: utf-8

from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.toutiao),
    url(r'^/email_logs$', views.email_logs),
    url(r'^/get_email_logs$', views.get_email_logs),
    url(r'^/get_statistics', views.get_statistics),

    url(r'^mem$', views.sett),
]
