# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

from django.conf import settings
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import DailyPerform


class DailyPerformSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyPerform
        fields = ('id', 'milk_intake', 'is_shit', 'shit_size', 'shit_color',
                  'is_urinate', 'urinate_size')
