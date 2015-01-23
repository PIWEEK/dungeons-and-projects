# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daprojects_core', '0005_auto_20150115_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='size',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='Arbitrary measure of directory size', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='module',
            name='size',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'size 1'), (2, 'size 2'), (5, 'size 5')], verbose_name='Size', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='issue',
            name='file_line',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='File line', null=True),
            preserve_default=True,
        ),
    ]
