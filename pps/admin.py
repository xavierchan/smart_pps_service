# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Products, Orders


admin.site.register(Products)
admin.site.register(Orders)
