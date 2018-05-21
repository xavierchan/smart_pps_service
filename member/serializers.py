# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

import models
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import GroupExtension


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    # captcha = serializers.CharField()

    def _check_old_password(self, old_password):
        pass

    def _check_captcha(self, capthca):
        pass

    def validate(self, attrs):
        self._check_captcha(attrs['captcha'])
        self._check_old_password(attrs['old_password'])
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    group_type = serializers.IntegerField(source='extension.group_type')

    class Meta:
        model = Group
        fields = ('id', 'name', 'group_type')


class OrganizationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        org = models.Organizations.objects.create(**validated_data)
        return org

    class Meta:
        model = models.Organizations
        fields = ('id', 'name', 'alias', 'crt')


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='profile.gender')
    mobile = serializers.CharField(source='profile.mobile')
    wx_open_id = serializers.CharField(source='profile.wx_open_id')

    class Meta:
        model = User
        fields = ('id', 'username', 'gender', 'email', 'mobile', 'wx_open_id')
