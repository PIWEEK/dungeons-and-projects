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
        ordering = ('slug',)

    class MPTTMeta:
        order_insertion_by = ('slug',)

    def __str__(self):
        return self.slug

