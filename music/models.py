# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Music(models.Model):
    name = models.CharField(verbose_name='名称', max_length=100)
    singer = models.CharField(verbose_name='歌手', max_length=50)
    duration = models.IntegerField(verbose_name='时长', default=0)
    album = models.CharField(verbose_name='专辑', max_length=100)
    url = models.CharField(verbose_name='url', max_length=1000)

    class Meta:
        verbose_name = '歌曲'
        verbose_name_plural = verbose_name
