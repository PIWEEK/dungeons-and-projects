import os
import re

from daprojects_python import resources

DEFAULT_IGNORE_LIST = [
    '.git',
    '__pycache__',
    '.*\.egg-info',
]

def read_tree_structure(root_path, depth=3, ignore_list=[]):
    directory_tree = _read_directory_level(root_path, depth, DEFAULT_IGNORE_LIST + ignore_list)
    return directory_tree


def _read_directory_level(path, depth, ignore_list):
    print(path) # TODO 1: use callback to send the event to the caller
    if depth <= 0:
        return []
    else:
        return [
            {
                'name': dir_name,
                'subdirs': _read_directory_level(os.path.join(path, dir_name), depth-1, ignore_list),
            }
            for dir_name in os.listdir(path)
            if os.path.isdir(os.path.join(path, dir_name)) and not _ignore_matches(dir_name, ignore_list)
        ]


def _ignore_matches(file_name, ignore_list):
    return any([re.match(pattern, file_name) for pattern in ignore_list])


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
        _analyze_dir(module, os.path.join(root_path, directory.path), directory.is_leaf_node, issues)

    return issues


def _analyze_dir(module, dir_path, recursive, issues):
    for filename in [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]:
        issues.extend(
            _analyze_file(module, os.path.join(dir_path, filename))
        )
    if recursive:
        for subdir in [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]:
            _analyze_dir(module, os.path.join(dir_path, subdir), True, issues)


def _analyze_file(module, file_path):
    root, ext = os.path.splitext(file_path)
    if ext == '.py':
        return _analyze_file_python(module, file_path)
    elif ext == '.coffee':
        return _analyze_file_coffeescript(module, file_path)
    elif ext == '.html':
        return _analyze_file_html(module, file_path)
    else:
        # TODO: add more source code file types
        return []


def _analyze_file_python(module, file_path):
    return _analyze_file_regex(module, file_path, [r'# *{} *(?P<size>[1-5]?):? *(?P<description>.*)'])


def _analyze_file_coffeescript(module, file_path):
    return _analyze_file_regex(module, file_path, [r'# *{} *(?P<size>[1-5]?):? *(?P<description>.*)'])


def _analyze_file_html(module, file_path):
    return _analyze_file_regex(module, file_path, [
        r'<!-- *{} *(?P<size>[1-5]?):? *(?P<description>.*) *-->.*',
        r'{{# *{} *(?P<size>[1-5]?):? *(?P<description>.*) *#}}.*',
        r'{{% *comment *%}} *{} *(?P<size>[1-5]?):? *(?P<description>.*) *{{% *endcomment *%}}.*'
    ])


def _analyze_file_regex(module, file_path, regexps):
    # TODO 3: move this to a more external context, for it not to be loaded for each analyzed file
    kind_exps = [
        (issue_kind, [re.compile(regexp.format(issue_kind.name)) for regexp in regexps])
        for issue_kind in resources.list_issue_kinds()
    ]

    issues = []

    with open(file_path, 'r') as file:
        for i, line in enumerate(file.readlines()):
            for (issue_kind, exps) in kind_exps:
                for exp in exps:
                    for match in exp.finditer(line):
                        _add_issue(
                            issues,
                            module,
                            file_name=os.path.basename(file_path),
                            file_line=i+1,
                            description=match.group('description'),
                            issue_kind=issue_kind,
                            size=int(match.group('size')) if match.group('size') else None,
                        )

    return issues


def _add_issue(issues, module, file_name, file_line, description, issue_kind, size):
    issues.append({
        'module': module.url,
        'file_name': file_name,
        'file_line': file_line,
        'description': description,
        'kind': issue_kind.url,
        'size': size,
    })
    # TODO 1: use callback to send the event to the caller
    print('{}: {}({}) - {} {}'.format(
        module.path,
        file_name,
        file_line,
        size,
        issue_kind.name,
    ))

