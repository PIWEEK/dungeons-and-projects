from django.db import models
from django.utils.translation import ugettext_lazy as _

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
        return self.slug


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
    name = models.CharField(
        max_length=255, blank=True, null=False,  # issues may have no name
        verbose_name=_('Name')
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
        return _('Issue {} - {}').format(self.module.slug, self.id)

