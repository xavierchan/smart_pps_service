# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Job(models.Model):
    url = models.CharField(max_length=100, verbose_name='链接')
    company = models.CharField(max_length=50, verbose_name='公司')
    name = models.CharField(max_length=50, verbose_name='名称')
    salary = models.CharField(max_length=50, verbose_name='薪资')
    area = models.CharField(max_length=50, verbose_name='地区')
    exp = models.CharField(max_length=50, verbose_name='经验')
    education = models.CharField(max_length=50, verbose_name='学历')
    type = models.CharField(max_length=50, verbose_name='性质')
    tags = models.CharField(max_length=100, verbose_name='标签')
    advantage = models.TextField(verbose_name='优势')
    bt = models.TextField(verbose_name='职位描述')
    work_place = models.CharField(max_length=50, verbose_name='工作地点')

    class Meta:
        verbose_name = '岗位'
        verbose_name_plural = '岗位'


class Company(models.Model):
    url = models.CharField(max_length=100, verbose_name='链接')
    logo = models.CharField(max_length=50, verbose_name='公司')
    name = models.CharField(max_length=50, verbose_name='名称')
    domain = models.CharField(max_length=50, verbose_name='领域')
    stage = models.CharField(max_length=50, verbose_name='发展阶段')
    co_company = models.CharField(max_length=50, verbose_name='投资机构')
    size = models.CharField(max_length=50, verbose_name='规模')
    site = models.CharField(max_length=50, verbose_name='主页')

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = '公司'
