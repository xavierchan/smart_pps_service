# coding: utf-8

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^tags/$', views.get_tags, name='tags'),
    url(r'^categorys/$', views.get_categorys, name='categorys'),
    url(r'^(?P<id>(\d+))/$', views.detail),
]

