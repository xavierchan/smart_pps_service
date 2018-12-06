# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Game(models.Model):
    name = models.CharField(verbose_name='名称', max_length=100)

    class Meta:
        verbose_name = '游戏'
        verbose_name_plural = verbose_name
