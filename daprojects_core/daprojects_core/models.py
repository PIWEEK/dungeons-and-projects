from django.db import models
from django.utils.translation import ugettext_lazy as _

import itertools
import os

from mptt.models import MPTTModel, TreeForeignKey

class Project(models.Model):
    name = models.CharField(
        max_length=255, blank=False, null=False,
        verbose_name=_('Name')
    )
    slug = models.SlugField(
        max_length=255, blank=False, null=False, unique=True,
        verbose_name=_('Slug')
    )
    description = models.TextField(
        blank=True, null=False,
        verbose_name=_('Description')
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ('name',)

    def __str__(self):
        return _('project "{}"').format(self.name)

    def first_level_modules(self):
        return self.modules.filter(level=0)


class Module(MPTTModel):
    project = models.ForeignKey('Project',
        blank=False, null=False,
        related_name='modules',
        verbose_name=_('Project')
    )
    parent = TreeForeignKey('self',
        blank=True, null=True,
        related_name='children',
        verbose_name=_('Parent')
    )
    name = models.CharField(
        max_length=255, blank=True, null=False,  # modules may have no name
        verbose_name=_('Name')
    )
    slug = models.SlugField(
        max_length=255, blank=False, null=False,
        verbose_name=_('Slug')
    )
    description = models.TextField(
        blank=True, null=False,
        verbose_name=_('Description')
    )

    class Meta:
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')
        ordering = ('project', 'slug',)

    class MPTTMeta:
        order_insertion_by = ('project', 'slug',)

    def __str__(self):
        return self.path

    @property
    def path(self):
        return os.path.join(
            *[dir.slug for dir in self.get_ancestors(include_self=True)]
        )

    def nested_issues(self):
        return itertools.chain(*[model.issues.all() for model in self.get_descendants(include_self=True)])


class IssueKind(models.Model):
    name = models.CharField(
        max_length=255, blank=False, null=False,
        verbose_name=_('Name')
    )

    class Meta:
        verbose_name = _('Issue kind')
        verbose_name_plural = _('Issue kinds')
        ordering = ('name',)

    def __str__(self):
        return _('Issue kind "{}"').format(self.name)


class Issue(models.Model):
    module = models.ForeignKey('Module',
        blank=False, null=False,
        related_name='issues',
        verbose_name=_('Module')
    )
    file_name = models.CharField(
        max_length=255, blank=True, null=False,  # issues may have no file
        verbose_name=_('File name')
    )
    file_line = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('File line')
    )
    description = models.TextField(
        blank=True, null=False,
        verbose_name=_('Description')
    )
    kind = models.ForeignKey('IssueKind',
        blank=False, null=False,
        related_name='issues',
        verbose_name=_('Kind')
    )
    size = models.PositiveSmallIntegerField(
        blank=False, null=False,
        choices=(
            (1, 'level 1'),
            (2, 'level 2'),
            (3, 'level 3'),
            (4, 'level 4'),
            (5, 'level 5'),
        ),
        verbose_name=_('Size')
    )

    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')
        ordering = ('module', 'id')

    def __str__(self):
        return _('Issue {} - {}').format(self.module.path, self.kind.name)


class Directory(MPTTModel):
    project = models.ForeignKey('Project',
        blank=False, null=False,
        related_name='directories',
        verbose_name=_('Project')
    )
    parent = TreeForeignKey('self',
        blank=True, null=True,
        related_name='children',
        verbose_name=_('Parent')
    )
    slug = models.SlugField(
        max_length=255, blank=False, null=False,
        verbose_name=_('Slug')
    )
    modules = models.ManyToManyField('Module',
        blank=True, null=True,
        related_name='directories',
        verbose_name=_('Modules')
    )

    class Meta:
        verbose_name = _('Directory')
        verbose_name_plural = _('Directories')
        ordering = ('project', 'slug',)

    class MPTTMeta:
        order_insertion_by = ('project', 'slug',)

    def __str__(self):
        return self.slug

    @property
    def path(self):
        return os.path.join(
            *[dir.slug for dir in self.get_ancestors(include_self=True)]
        )

