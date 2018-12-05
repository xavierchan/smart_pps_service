# coding: utf-8

from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^tags/$', views.get_tags, name='blog_tags'),
    url(r'^categorys/$', views.get_categorys, name='blog_categorys'),
    url(r'^(?P<id>(\d+))/$', views.detail),
]
