from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Project, ProjectAdmin)


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 1


class ModuleAdmin(MPTTModelAdmin):
    model = Module
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('slug', 'level', 'size', 'project_name')
    list_filter = ('project__name', 'level')
    inlines = (IssueInline,)

    def project_name(self, obj):
        return obj.project.name

admin.site.register(Module, ModuleAdmin)


class IssueKindAdmin(admin.ModelAdmin):
    model = IssueKind

admin.site.register(IssueKind, IssueKindAdmin)


class DirectoryAdmin(MPTTModelAdmin):
    model = Directory
    list_display = ('slug', 'level', 'size', 'project_name')
    list_filter = ('project__name', 'level')
    filter_horizontal = ('modules',)

    def project_name(self, obj):
        return obj.project.name

admin.site.register(Directory, DirectoryAdmin)

