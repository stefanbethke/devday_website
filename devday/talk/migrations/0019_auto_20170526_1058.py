# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-26 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0018_talkmedia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talkmedia',
            name='slideshare',
            field=models.CharField(blank=True, max_length=64, verbose_name='Slideshare id'),
        ),
        migrations.AlterField(
            model_name='talkmedia',
            name='youtube',
            field=models.CharField(blank=True, max_length=64, verbose_name='Youtube video id'),
        ),
    ]
