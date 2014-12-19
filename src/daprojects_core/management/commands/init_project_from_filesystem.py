from django.core.management.base import BaseCommand, CommandError

import os

from daprojects_core import models, services


class Command(BaseCommand):
    args = '<project_slug> <filesystem_root>'
    help = '''
    Make an initial load of directories and modules of a project, by reading the
    physical directories of a filesystem. Need the project to be empty.
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

        init_project_from_filesystem(project, filesystem_root)


def init_project_from_filesystem(project, root_path, depth = 3):
    directory_tree = _read_directory_level(root_path, depth)
    services.init_project(project, directory_tree)


def _read_directory_level(path, depth):
    print(path) # TODO: use callback to send the event to the caller
    if depth <= 0:
        return []
    else:
        return [
            {
                'name': dir_name,
                'subdirs': _read_directory_level(os.path.join(path, dir_name), depth-1),
            }
            for dir_name in os.listdir(path) if os.path.isdir(os.path.join(path, dir_name))
        ]

