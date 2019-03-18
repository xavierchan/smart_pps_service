# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from common import BasePagination
from models import DailyPerform
import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class DailyPerformViewSet(viewsets.ModelViewSet):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = DailyPerform.objects.filter()
    serializer_class = serializers.DailyPerformSerializer
    pagination_class = BasePagination


def add(request):
    return render(request, 'baby_daily/add.html')
