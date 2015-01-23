from rest_framework import serializers

from daprojects_core.models import Project, Module, IssueKind, Issue, Directory


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    first_level_modules = serializers.HyperlinkedRelatedField(
        view_name='module-detail',
        read_only=True,
        many=True,
    )
    class Meta:
        model = Project
        fields = ('url', 'name', 'slug', 'description', 'first_level_modules')


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ('url', 'project', 'parent', 'children', 'name', 'slug', 'path', 'description', 'directories', 'issues')


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
        fields = ('url', 'project', 'parent', 'children', 'slug', 'path', 'modules', 'is_leaf_node')


class DirectoryTreeSerializer(serializers.Serializer):
    '''For project directory initialization'''
    name = serializers.CharField(max_length=255)
    size = serializers.IntegerField()

# You cannot declare a field whose type is the same serializer, so we add it later.
# See http://stackoverflow.com/questions/13376894/django-rest-framework-nested-self-referential-objects
DirectoryTreeSerializer._declared_fields['subdirs'] = DirectoryTreeSerializer(many=True)


class SyncIssueSerializer(serializers.HyperlinkedModelSerializer):
    '''For issues synchronization'''
    class Meta:
        model = Issue
        fields = ('file_name', 'file_line', 'description', 'kind', 'size')


class SyncModuleSerializer(serializers.Serializer):
    '''For issues synchronization'''
    module = serializers.HyperlinkedRelatedField(
        view_name='module-detail',
        queryset=Module.objects.all(),
    )
    issues = SyncIssueSerializer(many=True)
    class Meta:
        fields = ('module', 'issues', 'submodules')

SyncModuleSerializer._declared_fields['submodules'] = SyncModuleSerializer(many=True)

