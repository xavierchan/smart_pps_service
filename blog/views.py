# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from smart_pps_service.common import viewsets
from rest_framework import permissions
import serializers
from models import Article
from rest_framework import filters
from django.http.response import JsonResponse
from tasks import increate_pv
import datetime
datetime.timedelta(hours=1)

from smart_pps_service.common.common import md_2_html2, xresult


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
    categorys = list(
        set([item.get('category') for item in Article.objects.all().values('category') if item.get('category')]))
    return JsonResponse(data=xresult(data=categorys))


@csrf_exempt
def get_tags(request):
    tags = ",".join([item.get('tags') for item in Article.objects.all().values('tags') if item.get('tags')])
    tags = list(set(tags.split(',')))
    return JsonResponse(data=xresult(data=tags))


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.filter(is_published=True)
    serializer_class = serializers.ArticleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=category', 'tags')
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
