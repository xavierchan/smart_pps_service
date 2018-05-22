# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pytz import timezone

from django.contrib import admin
from django.conf import settings
import models


@admin.register(models.OssFile)
class OssFileAdmin(admin.ModelAdmin):
    list_display = ('fid', 'key', 'uploader_id', 'upload_time_show', 'upload_ip')
    ordering = ('-upload_time',)

    def upload_time_show(self, obj):
        return obj.upload_time.astimezone(tz=timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')
    upload_time_show.short_description = '上传时间'
