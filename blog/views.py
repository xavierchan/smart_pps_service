# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, filters, permissions
from rest_framework.response import Response

from common import BasePagination
from smart_pps_service.common import viewsets
from smart_pps_service.common.common import md_2_html2, xresult
import serializers
from models import Article
from tasks import increate_pv


def index(request):
    return render(request, 'blog/index.html')


@login_required
def manage(request):
    return render(request, 'blog/manage.html')


def detail(request, id):
    try:
        obj = Article.objects.get(id=id)
        increate_pv(id)
    except Exception as e:
        pass
    html5_content = md_2_html2(obj.content)
    return render(request, 'blog/detail.html', {
        'id': obj.id,
        'title': obj.title,
        'category': obj.category,
        'tags': obj.tags.split(','),
        'pv': obj.pv,
        'upt': obj.upt,
        'content': html5_content.replace('<table>', '<table class="table table-bordered table-striped">')
    })


@csrf_exempt
def get_categorys(request):
    categorys = list(set(Article.objects.filter(is_published=True).values_list('category',
                                                           flat=True)))
    if len(categorys[0]) == 0:
        categorys.remove(categorys[0])
    return JsonResponse(data=xresult(data=categorys))


@csrf_exempt
def get_tags(request):
    tags = ",".join(Article.objects.filter(is_published=True).values_list('tags', flat=True))
    tags = list(set(tags.split(',')))
    if len(tags[0]) == 0:
        tags.remove(tags[0])
    return JsonResponse(data=xresult(data=tags))


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.filter(is_published=True)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=category', 'tags')
    serializer_class = serializers.ArticleSerializer
    pagination_class = BasePagination
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
