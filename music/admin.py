# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Music, MusicsWebsite, CMusic


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'singer', 'duration', 'album')
    list_filter = ('singer', )
    search_fields = ('name', )
    list_per_page = 20


@admin.register(MusicsWebsite)
class MusicsWebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_', 'scraper')
    list_display_links = ('name',)

    def url_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.url, title=instance.url)

    url_.allow_tags = True


@admin.register(CMusic)
class CMusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'news_website', 'singer',)
    list_display_links = ('name',)
    raw_id_fields = ('checker_runtime',)
