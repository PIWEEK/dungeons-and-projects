from rest_framework import serializers

from daprojects_core.models import Project, Module, IssueKind, Issue, Directory


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('url', 'name', 'slug', 'description')


class DirectoryTreeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

# You cannot declare a field whose type is the same serializer, so we add it later.
# See http://stackoverflow.com/questions/13376894/django-rest-framework-nested-self-referential-objects
DirectoryTreeSerializer._declared_fields['subdirs'] = DirectoryTreeSerializer(many=True)


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ('url', 'project', 'parent', 'children', 'name', 'slug', 'description', 'directories', 'issues')


class IssueKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IssueKind
        fields = ('url', 'name')


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ('url', 'module', 'file_name', 'file_line', 'description', 'kind', 'size')


class DirectorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Directory
        fields = ('url', 'project', 'parent', 'children', 'slug', 'modules')

