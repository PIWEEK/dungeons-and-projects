from django.contrib import admin

from .models import *

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Project, ProjectAdmin)

