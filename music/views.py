# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from rest_framework import viewsets, filters, permissions

from common import BasePagination
from models import Music
import serializers


@login_required
def index(request):
    return render_to_response('music/index.html')


class MusicViewSet(viewsets.ModelViewSet):

    queryset = Music.objects.all()
    filter_backends = (filters.SearchFilter,)
    serializer_class = serializers.MusicSerializer
    pagination_class = BasePagination
    permission_classes = (permissions.IsAuthenticated,)
