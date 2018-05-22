# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class OssFile(models.Model):
    name = models.CharField(verbose_name=u'名称', max_length=100)
    size = models.CharField(verbose_name=u'大小', max_length=50)
    type = models.CharField(verbose_name=u'类型', max_length=100)
    key = models.CharField(verbose_name=u'key', max_length=500)
    fid = models.CharField(verbose_name=u'fid', max_length=40)
    uploader_id = models.CharField(verbose_name=u'上传用户ID', max_length=20)
    upload_time = models.DateTimeField(verbose_name=u'上传时间', auto_now_add=True)
    upload_ip = models.CharField(verbose_name=u'上传ip', max_length=40)

    class Meta:
        verbose_name = 'oss文件'
        verbose_name_plural = 'oss文件'
