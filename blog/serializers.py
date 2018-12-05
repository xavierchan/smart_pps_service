# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

from django.conf import settings
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import Article
FMT_DATE = settings.FMT_DATE


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    author_name = serializers.CharField(source='author.username')
    crt = serializers.DateTimeField(format=FMT_DATE, required=False, read_only=True)
    upt = serializers.DateTimeField(format=FMT_DATE, required=False, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'category', 'tags', 'author', 'author_name', 'pv', 'crt', 'upt')
