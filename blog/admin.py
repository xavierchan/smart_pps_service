# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'tags', 'author', 'is_published', 'is_spread', 'pv', 'uv')
