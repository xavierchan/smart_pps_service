# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.utils.safestring import mark_safe
from django.contrib import admin
from models import Comic, ComicChapter


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('id', 'cover_img', 'name', 'author', 'type', 'intro')
    readonly_fields = ['cover_img']
    list_per_page = 10

    def cover_img(self, obj):
        try:
            img = mark_safe('<img src="%s" width="100px" />' % (obj.cover,))
        except Exception as e:
            img = ''
        return img

    cover_img.short_description = '封面'
    cover_img.allow_tags = True


@admin.register(ComicChapter)
class ComicChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'comic_name', 'title', 'chapter', 'imgs')
    readonly_fields = ['imgs']
    list_filter = ('comic',)
    list_per_page = 10

    def comic_name(self, obj):
        return obj.comic.name

    comic_name.short_description = '漫画'
    comic_name.allow_tags = True
