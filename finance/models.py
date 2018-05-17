# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TradingRecords(models.Model):
    member = models.ForeignKey(User, verbose_name='会员')
    money = models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='金额')
    content = models.CharField(max_length=30, verbose_name='内容')
    type = models.CharField(max_length=2, verbose_name='类型')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now=True, verbose_name='更新时间')