# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daprojects_core', '0004_auto_20141216_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='size',
            field=models.PositiveSmallIntegerField(choices=[(1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4'), (5, 'level 5')], blank=True, verbose_name='Size', null=True),
            preserve_default=True,
        ),
    ]
