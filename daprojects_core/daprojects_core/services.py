import os

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
            _init_project_step(project, module, directory, os.path.join(path, entry), depth - 1)

