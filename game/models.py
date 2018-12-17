# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Game(models.Model):
    name = models.CharField(verbose_name='名称', max_length=100)
    cover = models.CharField(verbose_name='封面', max_length=500)
    slug = models.CharField(verbose_name='slug', max_length=50)

    class Meta:
        verbose_name = '游戏'
        verbose_name_plural = verbose_name
