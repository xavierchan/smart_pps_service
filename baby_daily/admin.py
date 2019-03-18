# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import DailyPerform


@admin.register(DailyPerform)
class DailyPerformAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'milk_intake', 'shit_size', 'shit_color',
                    'is_urinate', 'urinate_size')
    list_per_page = 20
