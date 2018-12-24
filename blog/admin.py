# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'tags', 'author', 'is_published', 'is_recommend', 'pv', 'uv', 'upt')
    list_display_links = ('title',)
    readonly_fields = ('pv', 'uv')
    list_filter = ('is_published', 'is_recommend', 'author')
    search_fields = ('title', )
    list_per_page = 20
