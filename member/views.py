# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
import models
import serializers


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (permissions.IsAuthenticated, )


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = models.Organizations.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated, )


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
