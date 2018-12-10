# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

from django.conf import settings
from rest_framework import serializers

from models import Music
FMT_DATE = settings.FMT_DATE


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id', 'name', 'singer', 'duration', 'album', 'url')
