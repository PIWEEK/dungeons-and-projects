from rest_framework import viewsets, filters, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from daprojects_core.models import Project, Module, IssueKind, Issue, Directory
from daprojects_core.services import init_project, sync_issues

from .serializers import (
    ProjectSerializer, ModuleSerializer, IssueKindSerializer, IssueSerializer, DirectorySerializer,
    DirectoryTreeSerializer, SyncModuleSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('slug',)

    @detail_route(methods=['post'])
    def initialize(self, request, pk=None):
        project = self.get_object()
        dir_tree_serializer = DirectoryTreeSerializer(data=request.data, many=True)
        if dir_tree_serializer.is_valid():
            init_project(project, dir_tree_serializer.validated_data)
            return Response({'status': 'Project initialized'})
        else:
            return Response(dir_tree_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def sync_issues(self, request, pk=None):
        project = self.get_object()
        sync_module_serializer = SyncModuleSerializer(data=request.data, many=True, context={'request': request})
        if sync_module_serializer.is_valid():
            sync_issues(project, sync_module_serializer.validated_data)
            return Response({'status': 'Project synchronized'})
        else:
            return Response(sync_module_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('slug', 'project', 'parent')


class IssueKindViewSet(viewsets.ModelViewSet):
    queryset = IssueKind.objects.all()
    serializer_class = IssueKindSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('module', 'kind', 'size')


class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('slug', 'project', 'parent')

