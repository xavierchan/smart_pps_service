# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-06 06:55
from __future__ import unicode_literals

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_add_promotion_attr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=mdeditor.fields.MDTextField(blank=True, verbose_name='\u5185\u5bb9'),
        ),
    ]
