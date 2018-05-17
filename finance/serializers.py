# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

import models
from rest_framework import serializers


class TradingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TradingRecords
        fields = ('id', 'money', 'content', 'type', 'crt')
