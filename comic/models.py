# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class TimestampModel(models.Model):
   crt = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, editable=False)
   upt = models.DateTimeField(verbose_name='更新时间', auto_now=True)

   class Meta:
       abstract = True


class Comic(TimestampModel):
    cover = models.CharField(verbose_name='封面', max_length=250, null=True)
    ac_id = models.CharField(verbose_name='ac_id', max_length=100)
    name = models.CharField(verbose_name='名称', max_length=100)
    intro = models.TextField(verbose_name='简介', max_length=1000, null=True)
    author = models.CharField(verbose_name='作者', max_length=50, null=True)
    type = models.IntegerField(verbose_name='类型', default=0)

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta:
        verbose_name_plural = verbose_name = '漫画'


class ComicChapter(TimestampModel):
    comic = models.ForeignKey(Comic, verbose_name='漫画', related_name='chapters')
    title = models.CharField(verbose_name='标题', max_length=100)
    ac_cid = models.CharField(verbose_name='ac_cid', max_length=100)
    chapter = models.IntegerField(verbose_name='章节')
    imgs = models.TextField(verbose_name='图片', max_length=2000)

    class Meta:
        verbose_name_plural = verbose_name = '漫画章节'
