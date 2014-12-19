from django.core.management.base import BaseCommand, CommandError

import os
import re
import random

from daprojects_core import models, services


class Command(BaseCommand):
    args = '<project_slug> <filesystem_root>'
    help = '''
    Search the filesystem for specific comments (see kinds) and create issues for them.
    '''

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('You must specify project slug and filesystem root.')

        project_slug = args[0]
        try:
            project = models.Project.objects.get(slug=project_slug)
        except models.Project.DoesNotExist:
            raise CommandError('Cannot find a project with slug "{}"'.format(project_slug))

        filesystem_root = args[1]
        if not os.access(filesystem_root, os.R_OK):
            raise CommandError('Cannot read path "{}"'.format(filesystem_root))

        sync_issues_with_filesystem(project, filesystem_root)


def sync_issues_with_filesystem(project, root_path):
    '''
    Search the filesystem for specific comments (see kinds) and create issues for them.
    '''
    modules_issues = _analyze_modules(project.first_level_modules(), root_path)
    services.sync_issues(project, modules_issues)


def _analyze_modules(modules, root_path):
    return [
        {
            'module': module,
            'issues': _analyze_module(module, root_path),
            'submodules': _analyze_modules(module.get_children(), root_path),
        }
        for module in modules
    ]


def _analyze_module(module, root_path):
    issues = []

    for directory in module.directories.all():
        for filename in os.listdir(os.path.join(root_path, directory.path)):
            issues.extend(
                _analyze_file(module, os.path.join(root_path, directory.path, filename))
            )

    return issues


def _analyze_file(module, file_path):
    root, ext = os.path.splitext(file_path)
    if ext == '.py':
        return _analyze_file_python(module, file_path)
    elif ext == '.coffee':
        return _analyze_file_coffeescript(module, file_path)
    elif ext == '.html':
        return _analyze_file_html(module, file_path)
    else:
        return []


def _analyze_file_python(module, file_path):
    return _analyze_file_regex(module, file_path, ['# *{}:? *(.*)'])


def _analyze_file_coffeescript(module, file_path):
    return _analyze_file_regex(module, file_path, ['# *{}:? *(.*)'])


def _analyze_file_html(module, file_path):
    return _analyze_file_regex(module, file_path, ['<!-- *{}:? *(.*) -->', '{{# *{}:? *(.*) *#}}', '{{% comment %}} *(.*) *{{% endcomment %}}'])


def _analyze_file_regex(module, file_path, regexps):
    issues = []

    with open(file_path, 'r') as file:
        content = file.read()
        for regexp in regexps:
            for issue_kind in models.IssueKind.objects.all():
                for match in re.finditer(regexp.format(issue_kind.name), content):
                    issues.append({
                        'module': module,
                        'file_name': os.path.basename(file_path),
                        'file_line': None, # TODO: calculate file line
                        'description': match.group(1),
                        'kind': issue_kind,
                        'size': random.randint(1, 5), # TODO: read size from comment text
                    })
                    # TODO: use callback to send the event to the caller
                    print('{} - {} {}'.format(
                        issues[-1]['module'].path,
                        issues[-1]['size'],
                        issues[-1]['kind'].name,
                    ))

    return issues

