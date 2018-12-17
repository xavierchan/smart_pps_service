# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from rest_framework import viewsets, views, filters, permissions
import requests

from common import BasePagination
from models import Music
import serializers


@login_required
def index(request):
    return render_to_response('music/index.html')


@login_required
def search(request):
    return render_to_response('music/search.html')


class MusicViewSet(viewsets.ModelViewSet):

    queryset = Music.objects.all()
    filter_backends = (filters.SearchFilter,)
    serializer_class = serializers.MusicSerializer
    pagination_class = BasePagination
    permission_classes = (permissions.IsAuthenticated,)


class SearchMusicViewSet(views.APIView):

    def list(self, request):
        search_name = request.GET.get('search_name')

