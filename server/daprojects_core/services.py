import os

from . import models


def init_project(project, directory_tree):
    '''
    Make an initial load of directories and modules of a project, from the specified
    directory tree structure. Need the project to be empty.

      - directory_tree is a list with the first level directories, each one having
        - name: the name of the directory
        - size: arbitrary size measure (e.g. number of files inside)
        - subdirs: a list of subdirectories, recursively with the same structure
    '''
    if project.modules.exists() or project.directories.exists():
        raise ValueError('The project must be empty')

    _init_project_level(project, None, None, directory_tree)

    _calculate_module_sizes(project)


def _init_project_level(project, parent_module, parent_dir, dir_level):
    for dir_data in dir_level:
        directory = models.Directory.objects.create(
            project = project,
            parent = parent_dir,
            slug = dir_data['name'],
            size = dir_data['size'],
        )
        module = models.Module.objects.create(
            project = project,
            parent = parent_module,
            slug = dir_data['name'],
            size = 1, # This is calculated later
        )
        directory.modules.add(module)
        _init_project_level(project, module, directory, dir_data['subdirs'])


def _calculate_module_sizes(project):
    size_limits = {}
    _initialize_module_sizes(project.first_level_modules.all(), size_limits)
    _calculate_ranges(size_limits)
    for level, sizes in size_limits.items():
        _make_sizes_proportional(project.first_level_modules.all(), size_limits)


def _initialize_module_sizes(modules, size_limits):
    for module in modules:
        module.size = sum([dir.size for dir in module.directories.all() if dir.size != None])
        module.save()

        if module.size > 0:
            if not module.level in size_limits:
                size_limits[module.level] = {'min': 999999999, 'max': 0}
            if module.size < size_limits[module.level]['min']:
                size_limits[module.level]['min'] = module.size
            if module.size > size_limits[module.level]['max']:
                size_limits[module.level]['max'] = module.size

        _initialize_module_sizes(module.children.all(), size_limits)


def _calculate_ranges(size_limits):
    for level, limits in size_limits.items():
        limits['range'] = limits['max'] - limits['min'] + 0.1


def _make_sizes_proportional(modules, size_limits):
    # Convert sizes from arbitrary range to 1, 2 ,3
    for module in modules:
        size_min = size_limits[module.level]['min']
        size_range = size_limits[module.level]['range']
        if size_range > 0 and size_range < 999999999:
            module.size = int((module.size - size_min) / size_range * 3) + 1
        else:
            import random # If no module has real size, set it randomly
            module.size = random.choice([1,2,3])
        module.save()
        _make_sizes_proportional(module.children.all(), size_limits)


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
        _sync_issues_module(module_data, project.first_level_modules, filter_kinds)


def _sync_issues_module(module_data, level_of_modules, filter_kinds):
    module = module_data['module']
    assert(module in level_of_modules)

    # TODO 2: synchronize instead of replacing
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

