# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from smart_pps_service.common import viewsets
from rest_framework import permissions
import serializers
from models import Article


def index(request):
    return render(request, 'blog/list.html')


def create(request):
    return render(request, 'blog/create.html')


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)
