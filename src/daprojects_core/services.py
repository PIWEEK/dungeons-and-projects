import os

from . import models


def init_project(project, directory_tree):
    '''
    Make an initial load of directories and modules of a project, from the specified
    directory tree structure. Need the project to be empty.

      - directory_tree is a list with the first level directories, each one having
        - name: the name of the directory
        - subdirs: a list of subdirectories, recursively with the same structure
    '''
    if project.modules.exists() or project.directories.exists():
        raise ValueError('The project must be empty')
    _init_project_level(project, None, None, directory_tree)


def _init_project_level(project, parent_module, parent_dir, dir_level):
    for dir_data in dir_level:
        directory = models.Directory.objects.create(
            project = project,
            parent = parent_dir,
            slug = dir_data['name'],
        )
        module = models.Module.objects.create(
            project = project,
            parent = parent_module,
            slug = dir_data['name'],
        )
        directory.modules.add(module)
        _init_project_level(project, module, directory, dir_data['subdirs'])


def sync_issues(project, modules_issues, filter_kinds=[]):
    '''
    Synchronize the issues of a project with the given list, by adding, updating
    and deleting issues as necessary.

      - modules_issues is a list of modules dictionaries, each one having
        - module: an instance of models.Module
        - issues: the desired list of issues, each one having
          - file_name
          - file_line
          - description
          - kind
          - size
        - submodules: a list of submodules, recursively with the same structure

     - filter_kinds is a list, if not empty only issues of these kinds are deleted
    '''
    for module_data in modules_issues:
        _sync_issues_module(module_data, project.first_level_modules(), filter_kinds)


def _sync_issues_module(module_data, level_of_modules, filter_kinds):
    module = module_data['module']
    assert(module in level_of_modules)

    # TODO: synchronize instead of replacing
    issues = module.issues.all()
    if filter_kinds:
        issues = issues.filter(kind__name__in=filter_kinds)
    issues.delete()

    for issue_data in module_data['issues']:
        issue = models.Issue.objects.create(
            module=module,
            file_name=issue_data['file_name'],
            file_line=issue_data['file_line'],
            description=issue_data['description'],
            kind=issue_data['kind'],
            size=issue_data['size'],
        )

    for submodule_data in module_data['submodules']:
        _sync_issues_module(submodule_data, module.get_children(), filter_kinds)

