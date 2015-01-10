# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('daprojects_core', '0002_initial_issue_kinds'),
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('modules', models.ManyToManyField(blank=True, to='daprojects_core.Module', null=True, verbose_name='Modules')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, related_name='children', to='daprojects_core.Directory', null=True, verbose_name='Parent')),
                ('project', models.ForeignKey(related_name='directories', to='daprojects_core.Project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Directory',
                'ordering': ('project', 'slug'),
                'verbose_name_plural': 'Directories',
            },
            bases=(models.Model,),
        ),
    ]
