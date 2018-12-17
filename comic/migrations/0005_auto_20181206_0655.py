# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-06 06:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0004_auto_20181204_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comicchapter',
            name='comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='comic.Comic', verbose_name='\u6f2b\u753b'),
        ),
    ]
