# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-07 21:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buildinfo', '0003_auto_20170119_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildinfo',
            name='raw_text',
        ),
    ]
