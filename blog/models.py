# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=20, verbose_name='标题')
    content = models.TextField(blank=True, verbose_name='内容')
    category = models.CharField(max_length=20, blank=True, verbose_name='分类')
    tags = models.CharField(max_length=20, blank=True, verbose_name='标签')
    crt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    upt = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
