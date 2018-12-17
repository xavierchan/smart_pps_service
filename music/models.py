# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem


class Music(models.Model):
    name = models.CharField(verbose_name='名称', max_length=100)
    singer = models.CharField(verbose_name='歌手', max_length=50)
    duration = models.IntegerField(verbose_name='时长', default=0)
    album = models.CharField(verbose_name='专辑', max_length=100)
    url = models.CharField(verbose_name='url', max_length=1000)

    class Meta:
        verbose_name = '歌曲'
        verbose_name_plural = verbose_name


class MusicsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class CMusic(models.Model):
    news_website = models.ForeignKey(MusicsWebsite)
    name = models.CharField(verbose_name='名称', max_length=100)
    singer = models.CharField(verbose_name='歌手', max_length=50)
    duration = models.IntegerField(verbose_name='时长', default=0)
    album = models.CharField(verbose_name='专辑', max_length=100)
    url = models.CharField(verbose_name='url', max_length=1000)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class CMusicItem(DjangoItem):
    django_model = CMusic
