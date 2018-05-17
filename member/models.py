# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Groups(models.Model):
    alias = models.CharField(max_length=20, verbose_name='别名')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class MemberProfile(models.Model):
    member = models.ForeignKey(User, verbose_name='会员')
    wx_open_id = models.CharField(max_length=30, verbose_name='wx_open_id')
    wx_union_id = models.CharField(max_length=30, blank=True, verbose_name='wx_union_id')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now=True, verbose_name='更新时间')
