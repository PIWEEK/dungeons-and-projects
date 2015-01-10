# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def initial_kinds(apps, schema_editor):
    IssueKind = apps.get_model('daprojects_core', 'IssueKind')
    IssueKind.objects.create(name='FIXME')
    IssueKind.objects.create(name='TODO')
    IssueKind.objects.create(name='NOTE')

class Migration(migrations.Migration):

    dependencies = [
        ('daprojects_core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_kinds),
    ]
