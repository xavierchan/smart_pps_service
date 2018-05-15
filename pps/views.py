# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import serializers
import models


class ProductViewSet(viewsets.ModelViewSet):

    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = models.Orders.objects.all()
    serializer_class = serializers.OrderSerializer
