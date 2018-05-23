# coding: utf-8

from django.conf.urls import url
import views


urlpatterns = [
    url(r'^get_upload_policy', views.get_upload_policy),
    url(r'^notify', views.notify),
    url(r'^list', views.file_list)
    # url(r'^upload/', views.upload),
]
