# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Group(models.Model):
    alias = models.CharField(max_length=20, verbose_name='别名')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now_add=True, auto_now=True, verbose_name='更新时间')
