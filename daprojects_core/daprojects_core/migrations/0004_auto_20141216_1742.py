# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daprojects_core', '0003_directory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='name',
        ),
        migrations.AddField(
            model_name='issue',
            name='file_line',
            field=models.IntegerField(blank=True, null=True, verbose_name='File line'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='file_name',
            field=models.CharField(default='', verbose_name='File name', max_length=255, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='directory',
            name='modules',
            field=models.ManyToManyField(blank=True, related_name='directories', to='daprojects_core.Module', null=True, verbose_name='Modules'),
            preserve_default=True,
        ),
    ]
