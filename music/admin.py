# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Music


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'singer', 'duration', 'album')
    list_per_page = 10
