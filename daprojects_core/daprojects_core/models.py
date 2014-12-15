from django.db import models
from django.utils.translation import ugettext_lazy as _

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

