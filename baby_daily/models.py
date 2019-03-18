# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DailyPerform(models.Model):

    milk_intake = models.IntegerField(verbose_name='吃奶量')
    is_shit = models.BooleanField(verbose_name='是否拉屎', default=True)
    shit_size = models.CharField(verbose_name='屎量', max_length=50, blank=True)
    shit_color = models.CharField(verbose_name='屎颜色', max_length=50,
                                  blank=True)
    is_urinate = models.BooleanField(verbose_name='是否拉尿', default=True)
    urinate_size = models.CharField(verbose_name='尿量', max_length=50,
                                    blank=True)
    time = models.DateTimeField(verbose_name='活动时间', auto_now=True)

    class Meta:
        verbose_name = '日常表现'
        verbose_name_plural = verbose_name
