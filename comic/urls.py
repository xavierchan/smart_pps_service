# coding: utf-8

from django.conf.urls import url
import views


urlpatterns = [
    url(r'', views.index),
    url(r'^(?P<id>(\d+))/chapters/$', views.chapters, name='comic_chapters'),
]
