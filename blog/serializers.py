# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

import models
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'category', 'tags', 'crt', 'upt')
