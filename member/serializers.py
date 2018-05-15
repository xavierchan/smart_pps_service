# coding: utf-8
# @Time    : 2018/05/15 19:08
# @Author  : xavier

import models
from rest_framework import serializers


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
    class Meta:
        model = models.Groups
        fields = ('id', 'crt')
