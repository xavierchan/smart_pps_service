# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-15 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='cover',
            field=models.CharField(default='', max_length=500, verbose_name='\u5c01\u9762'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.CharField(default='', max_length=50, verbose_name='slug'),
            preserve_default=False,
        ),
    ]
