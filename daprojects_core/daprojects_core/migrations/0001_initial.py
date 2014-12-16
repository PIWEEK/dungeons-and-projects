# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('size', models.PositiveSmallIntegerField(choices=[(1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4'), (5, 'level 5')], verbose_name='Size')),
            ],
            options={
                'verbose_name_plural': 'Issues',
                'ordering': ('module', 'id'),
                'verbose_name': 'Issue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueKind',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Issue kinds',
                'ordering': ('name',),
                'verbose_name': 'Issue kind',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', to='daprojects_core.Module', blank=True, null=True, verbose_name='Parent')),
            ],
            options={
                'verbose_name_plural': 'Modules',
                'ordering': ('project', 'slug'),
                'verbose_name': 'Module',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name_plural': 'Projects',
                'ordering': ('name',),
                'verbose_name': 'Project',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='module',
            name='project',
            field=models.ForeignKey(related_name='modules', to='daprojects_core.Project', verbose_name='Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='kind',
            field=models.ForeignKey(related_name='issues', to='daprojects_core.IssueKind', verbose_name='Kind'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='module',
            field=models.ForeignKey(related_name='issues', to='daprojects_core.Module', verbose_name='Module'),
            preserve_default=True,
        ),
    ]
