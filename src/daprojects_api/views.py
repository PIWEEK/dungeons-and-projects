from rest_framework import viewsets

from daprojects_core.models import Project, Module, IssueKind, Issue, Directory

from .serializers import (
    ProjectSerializer, ModuleSerializer, IssueKindSerializer, IssueSerializer, DirectorySerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class IssueKindViewSet(viewsets.ModelViewSet):
    queryset = IssueKind.objects.all()
    serializer_class = IssueKindSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

