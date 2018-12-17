# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

from django.conf import settings
from rest_framework import serializers

from models import Game


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'name', 'slug', 'cover')
