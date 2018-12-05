# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.utils.safestring import mark_safe
from django.contrib import admin
from models import Comic, ComicChapter


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('cover_img', 'name', 'author', 'type', 'intro')
    readonly_fields = ['cover_img']

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
    list_display = ('comic', 'chapter', 'imgs')
    readonly_fields = ['imgs']

#    def img_list(self, obj):
#        imgs = list(obj.imgs)
#        return [mark_safe('<img src="{}" width="100px" />'.format(img)) for img in imgs.values()]
#
#    img_list.short_description = '封面'
#    img_list.allow_tags = True
