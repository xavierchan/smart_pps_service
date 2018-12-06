# coding: utf-8
# @Time    : 2018/5/16 21:12
# @Author  : xavier

from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
