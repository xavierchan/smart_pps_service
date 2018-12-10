# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

import serializers
from common import BasePagination
from models import Comic


@login_required
def index(request):
    return render_to_response('comic/index.html')


@login_required
def chapters(request, id):
    comic = Comic.objects.get(id=id)
    return render_to_response('comic/chapters.html', {
        'comic': comic
    })


@login_required
def chapter_detail(request):
    return render_to_response('comic/chapter_detail.html')


class ComicViewSet(viewsets.ModelViewSet):

    queryset = Comic.objects.all()
    filter_backends = (filters.SearchFilter,)
    serializer_class = serializers.ComicSerializer
    pagination_class = BasePagination
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(methods=['GET'], url_path='(?P<pk>(\d+))/chapters/')
    def chapters(self, request, pk):
        queryset = self.get_object().chapters.order_by('chapter')
        serializer = serializers.ComicChapterSerializer(queryset, many=True)
        return Response(serializer.data)
