# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-10 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20181206_0655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_spread',
        ),
        migrations.AddField(
            model_name='article',
            name='is_recommend',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u63a8\u8350'),
        ),
    ]
