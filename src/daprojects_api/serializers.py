from rest_framework.serializers import HyperlinkedModelSerializer

from daprojects_core.models import Project, Module, IssueKind, Issue, Directory


class ProjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('url', 'name', 'slug', 'description')


class ModuleSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ('url', 'project', 'parent', 'children', 'name', 'slug', 'description', 'directories', 'issues')


class IssueKindSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = IssueKind
        fields = ('url', 'name')


class IssueSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ('url', 'module', 'file_name', 'file_line', 'description', 'kind', 'size')


class DirectorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Directory
        fields = ('url', 'project', 'parent', 'children', 'slug', 'modules')

