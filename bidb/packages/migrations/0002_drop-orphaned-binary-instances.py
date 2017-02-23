# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations

def forward(apps, schema_editor):
    Binary = apps.get_model('packages', 'Binary')

    Binary.objects.filter(generated_binaries__isnull=True).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
         migrations.RunPython(forward),
    ]
