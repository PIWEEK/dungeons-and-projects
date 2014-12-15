from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Project, ProjectAdmin)


class ModuleAdmin(MPTTModelAdmin):
    model = Module
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('slug', 'level', 'project_name')
    list_filter = ('project__name', 'level')

    def project_name(self, obj):
        return obj.project.name

admin.site.register(Module, ModuleAdmin)

