# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

from django.conf import settings
from rest_framework import serializers

from models import Comic
FMT_DATE = settings.FMT_DATE


class ComicSerializer(serializers.ModelSerializer):
    upt = serializers.DateTimeField(format=FMT_DATE, required=False, read_only=True)

    class Meta:
        model = Comic
        fields = ('id', 'name', 'cover', 'intro', 'upt')
