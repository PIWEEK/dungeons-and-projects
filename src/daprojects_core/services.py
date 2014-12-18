import os
import re
import random

from . import models

def init_project_from_filesystem(project, root_path, depth = 3):
    '''
    Make an initial load of directories and modules of a project, by reading the
    physical directories of a filesystem. Need the project to be empty.
    '''
    if project.modules.exists() or project.directories.exists():
        raise ValueError('The project must be empty')
    _init_project_step(project, None, None, root_path, depth)


def _init_project_step(project, parent_module, parent_dir, path, depth):
    if depth > 0:
        entries = [entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]
        entries.sort()
        for entry in entries:
            directory = models.Directory.objects.create(
                project = project,
                parent = parent_dir,
                slug = entry,
            )
            module = models.Module.objects.create(
                project = project,
                parent = parent_module,
                slug = entry,
            )
            directory.modules.add(module)
            print(str(module)) # TODO: use callback to send the event to the caller
            _init_project_step(project, module, directory, os.path.join(path, entry), depth - 1)


def sync_issues_with_filesystem(project, root_path):
    '''
    Search the filesystem for specific comments (see kinds) and create issues for them.
    '''
    for module in project.modules.all():
        # TODO: synchronize instead of replacing
        module.issues.all().delete()
        for directory in module.directories.all():
            for filename in os.listdir(os.path.join(root_path, directory.path)):
                _analyze_file(module, os.path.join(root_path, directory.path, filename))


def _analyze_file(module, file_path):
    root, ext = os.path.splitext(file_path)
    if ext == '.py':
        _analyze_file_python(module, file_path)
    elif ext == '.coffee':
        _analyze_file_coffeescript(module, file_path)
    elif ext == '.html':
        _analyze_file_html(module, file_path)


def _analyze_file_python(module, file_path):
    _analyze_file_regex(module, file_path, ['# *{}:? *(.*)'])


def _analyze_file_coffeescript(module, file_path):
    _analyze_file_regex(module, file_path, ['# *{}:? *(.*)'])


def _analyze_file_html(module, file_path):
    _analyze_file_regex(module, file_path, ['<!-- *{}:? *(.*) -->', '{{# *{}:? *(.*) *#}}', '{{% comment %}} *(.*) *{{% endcomment %}}'])


def _analyze_file_regex(module, file_path, regexps):
    file = open(file_path, 'r')
    content = file.read()
    for regexp in regexps:
        for issue_kind in models.IssueKind.objects.all():
            for match in re.finditer(regexp.format(issue_kind.name), content):
                issue = models.Issue.objects.create(
                    module=module,
                    file_name=os.path.basename(file_path),
                    file_line=None, # TODO: calculate file line
                    description=match.group(1),
                    kind=issue_kind,
                    size=random.randint(1, 5), # TODO: read size from comment text
                )
                print(str(issue)) # TODO: use callback to send the event to the caller
