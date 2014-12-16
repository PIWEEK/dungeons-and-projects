from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from . import models

class HomeView(TemplateView):
    template_name = 'daprojects_core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = models.Project.objects.all()
        return context


class ProjectView(TemplateView):
    template_name = 'daprojects_core/project.html'

    def get_context_data(self, project_id=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(models.Project, pk=project_id)
        context['project'] = project
        return context


class ModuleView(TemplateView):
    template_name = 'daprojects_core/module.html'

    def get_context_data(self, project_id=None, module_id=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(models.Project, pk=project_id)
        module = get_object_or_404(models.Module, pk=module_id, project=project)
        context['project'] = project
        context['module'] = module
        return context

