# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.safestring import mark_safe

from models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'cover_img', 'slug', 'name')
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
