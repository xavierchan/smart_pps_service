# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import models
import serializers


class TradingRecordViewSet(viewsets.ModelViewSet):

    queryset = models.TradingRecords.objects.all()
    serializer_class = serializers.TradingRecordSerializer
