import os
import re

from daprojects_python import resources

def read_tree_structure(root_path, depth = 3):
    directory_tree = _read_directory_level(root_path, depth)
    return directory_tree


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


def find_module_issues(project, root_path):
    '''
    Search the filesystem for specific comments (see kinds) and create issues for them.
    '''
    modules = [resources.retrieve_module(m) for m in project.first_level_modules]
    module_structure = _analyze_modules(modules, root_path)
    return module_structure


def _analyze_modules(modules, root_path):
    return [
        {
            'module': module.url,
            'issues': _analyze_module(module, root_path),
            'submodules': _analyze_modules([resources.retrieve_module(sm) for sm in module.children], root_path),
        }
        for module in modules
    ]


def _analyze_module(module, root_path):
    issues = []

    for directory in [resources.retrieve_directory(d) for d in module.directories]:
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
            for issue_kind in resources.list_issue_kinds():
                for match in re.finditer(regexp.format(issue_kind.name), content):
                    issues.append({
                        'module': module.url,
                        'file_name': os.path.basename(file_path),
                        'file_line': None, # TODO: calculate file line
                        'description': match.group(1),
                        'kind': issue_kind.url,
                        'size': 1,
                    })
                    # TODO: use callback to send the event to the caller
                    print('{} - {} {}'.format(
                        module.path,
                        issues[-1]['size'],
                        issue_kind.name,
                    ))

    return issues

