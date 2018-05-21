# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.db import models


class GroupExtension(models.Model):
    GROUP_TYPE = (
        (0, '拥有者'),
        (1, '管理者'),
        (2, '成员'),
    )
    group = models.OneToOneField(Group, verbose_name='组', related_name='extension', primary_key=True)
    group_type = models.IntegerField(choices=GROUP_TYPE, verbose_name='分组类型')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class MemberProfile(models.Model):
    member = models.OneToOneField(User, verbose_name='会员', related_name='profile', primary_key=True)
    gender = models.CharField(max_length=1, verbose_name='性别')
    mobile = models.CharField(max_length=20, verbose_name='手机')
    wx_open_id = models.CharField(max_length=30, verbose_name='wx_open_id')
    wx_union_id = models.CharField(max_length=30, blank=True, verbose_name='wx_union_id')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class Organizations(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    alias = models.CharField(max_length=50, blank=True, verbose_name='别名')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now=True, verbose_name='更新时间')
