# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import models
import serializers


class GroupViewSet(viewsets.ModelViewSet):

    queryset = models.Groups.objects.all()
    serializer_class = serializers.GroupSerializer
