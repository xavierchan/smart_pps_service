# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from rest_framework import viewsets, filters, permissions

from common import BasePagination
from models import Game
import serializers


def index(request):
    return render_to_response('game/index.html')


class GameViewSet(viewsets.ModelViewSet):

    queryset = Game.objects.all()
    filter_backends = (filters.SearchFilter,)
    serializer_class = serializers.GameSerializer
    pagination_class = BasePagination
    permission_classes = (permissions.AllowAny,)

