# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from smart_pps_service.common import viewsets
from rest_framework import permissions
import serializers
from models import Article


@login_required
def index(request):
    return render(request, 'blog/list.html')


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)
