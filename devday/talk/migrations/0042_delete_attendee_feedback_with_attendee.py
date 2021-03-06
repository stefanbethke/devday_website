# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 12:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("attendee", "0009_auto_20181020_0802"),
        ("event", "0007_event_voting_open"),
        ("talk", "0041_drop_unique_constraint_on_talkslot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendeefeedback",
            name="attendee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="attendee.Attendee",
                verbose_name="Attendee",
            ),
        )
    ]
