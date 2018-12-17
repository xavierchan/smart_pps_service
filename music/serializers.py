# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

from rest_framework import serializers

from models import Music


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id', 'name', 'singer', 'duration', 'album', 'url')
