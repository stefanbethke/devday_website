# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-10 21:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20181010_1702'),
        ('speaker', '0002_migrate_speakers_from_talk_app'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='publishedspeaker',
            unique_together=set([('slug', 'event')]),
        ),
    ]
