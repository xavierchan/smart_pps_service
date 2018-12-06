# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from rest_framework import viewsets, filters, permissions

import serializers
from common import BasePagination
from models import Comic


def index(request):
    return render_to_response('comic/index.html')


def chapters(request):
    return render_to_response('comic/chapters.html')


def chapter_detail(request):
    return render_to_response('comic/chapter_detail.html')


class ComicViewSet(viewsets.ModelViewSet):

    queryset = Comic.objects.all()
    filter_backends = (filters.SearchFilter,)
    serializer_class = serializers.ComicSerializer
    pagination_class = BasePagination
    permission_classes = (permissions.AllowAny,)
