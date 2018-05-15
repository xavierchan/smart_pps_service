# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

import models
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Products
        fields = ('id', 'name', 'crt')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Orders
        fields = ('id', 'crt')
