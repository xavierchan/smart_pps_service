# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from smart_pps_service.common import viewsets
from rest_framework import permissions
import serializers
from models import Article
from smart_pps_service.common.common import md_2_html2


@login_required
def manage(request):
    return render(request, 'blog/manage.html')


def index(request):
    return render(request, 'blog/list.html')


def detail(request, id):
    try:
        obj = Article.objects.get(id=id)
    except Exception as e:
        pass
    html5_content = md_2_html2(obj.content)
    return render(request, 'blog/detail.html', {
        'id': obj.id,
        'title': obj.title,
        'category': obj.category,
        'tags': obj.tags.split(','),
        'upt': obj.upt,
        'content': html5_content.replace('<table>', '<table class="table table-bordered table-striped">')
    })


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)
