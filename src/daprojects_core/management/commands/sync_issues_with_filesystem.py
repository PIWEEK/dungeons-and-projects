from django.core.management.base import BaseCommand, CommandError

import os

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

        services.sync_issues_with_filesystem(project, filesystem_root)

