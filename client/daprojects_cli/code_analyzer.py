import os
import re


class SourceTreeAnalyzer:
    '''
    Walks a directory tree up to the given depth, and builds a structure with all the
    found directories and their sizes.
    '''

    DEFAULT_IGNORE_LIST = [
        '.git',
        '__pycache__',
        '.*\.egg-info',
    ]

    def __init__(self, root_path, depth=3, ignore_list = []):
        self._ignore_list = self.DEFAULT_IGNORE_LIST + ignore_list
        self._tree_structure = self._read_directory_level(root_path, depth)

    @property
    def tree_structure(self):
        return self._tree_structure

    def _read_directory_level(self, path, depth):
        print(path) # TODO 1: use callback to send the event to the caller
        if depth <= 0:
            return []
        else:
            directory_level = [
                {
                    'name': dir_name,
                    'subdirs': self._read_directory_level(os.path.join(path, dir_name), depth-1),
                }
                for dir_name in os.listdir(path)
                if os.path.isdir(os.path.join(path, dir_name)) and not self._ignore_matches(dir_name)
            ]
            for directory in directory_level:
                directory['size'] = (
                    self._directory_size(os.path.join(path, directory['name'])) +
                    sum((subdir['size'] for subdir in directory['subdirs'])) +
                    (self._recursive_subdir_size(os.path.join(path, directory['name'])) if depth == 1 else 0)
                )

            return directory_level

    def _ignore_matches(self, file_name):
        return any([re.match(pattern, file_name) for pattern in self._ignore_list])

    def _directory_size(self, path):
        # Simple approach: directory size is the number of source code files inside it
        # TODO 4: make a modular approach to allow adding file extensions by plugins
        return len([
            entry for entry in os.listdir(path)
            if os.path.isfile(os.path.join(path, entry))
               and any([re.match(pattern, entry) for pattern in ['.*\.py$','.*\.coffee$',  '.*\.html$']])
        ])

    def _recursive_subdir_size(self, path):
        return sum([
            self._directory_size(os.path.join(path, subdir)) + self._recursive_subdir_size(os.path.join(path, subdir))
            for subdir in os.listdir(path)
            if os.path.isdir(os.path.join(path, subdir)) and not self._ignore_matches(subdir)
        ])


class SourceCodeAnalyzer:
    '''
    Search the filesystem for specific comments (see kinds) and convert them into issues.
    '''
    def __init__(self, project, root_path, api):
        self._api = api
        modules = [self._api.modules.retrieve(m) for m in project.first_level_modules]
        self._module_structure = self._analyze_modules(modules, root_path)

    @property
    def module_structure(self):
        return self._module_structure

    def _analyze_modules(self, modules, root_path):
        return [
            {
                'module': module.url,
                'issues': self._analyze_module(module, root_path),
                'submodules': self._analyze_modules([self._api.modules.retrieve(sm) for sm in module.children], root_path),
            }
            for module in modules
        ]

    def _analyze_module(self, module, root_path):
        issues = []

        for directory in [self._api.directories.retrieve(d) for d in module.directories]:
            self._analyze_dir(module, os.path.join(root_path, directory.path), directory.is_leaf_node, issues)

        return issues

    def _analyze_dir(self, module, dir_path, recursive, issues):
        for filename in [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]:
            issues.extend(
                self._analyze_file(module, os.path.join(dir_path, filename))
            )
        if recursive:
            for subdir in [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]:
                self._analyze_dir(module, os.path.join(dir_path, subdir), True, issues)

    def _analyze_file(self, module, file_path):
        root, ext = os.path.splitext(file_path)
        if ext == '.py':
            return self._analyze_file_python(module, file_path)
        elif ext == '.coffee':
            return self._analyze_file_coffeescript(module, file_path)
        elif ext == '.html':
            return self._analyze_file_html(module, file_path)
        else:
            # TODO: add more source code file types
            return []

    def _analyze_file_python(self, module, file_path):
        return self._analyze_file_regex(module, file_path, [r'# *{} *(?P<size>[1-5]?):? *(?P<description>.*)'])

    def _analyze_file_coffeescript(self, module, file_path):
        return self._analyze_file_regex(module, file_path, [r'# *{} *(?P<size>[1-5]?):? *(?P<description>.*)'])

    def _analyze_file_html(self, module, file_path):
        return self._analyze_file_regex(module, file_path, [
            r'<!-- *{} *(?P<size>[1-5]?):? *(?P<description>.*) *-->.*',
            r'{{# *{} *(?P<size>[1-5]?):? *(?P<description>.*) *#}}.*',
            r'{{% *comment *%}} *{} *(?P<size>[1-5]?):? *(?P<description>.*) *{{% *endcomment *%}}.*'
        ])

    def _analyze_file_regex(self, module, file_path, regexps):
        # TODO 3: move this to a more external context, for it not to be loaded for each analyzed file
        kind_exps = [
            (issue_kind, [re.compile(regexp.format(issue_kind.name)) for regexp in regexps])
            for issue_kind in self._api.issue_kinds.list()
        ]

        issues = []

        with open(file_path, 'r') as file:
            for i, line in enumerate(file.readlines()):
                for (issue_kind, exps) in kind_exps:
                    for exp in exps:
                        for match in exp.finditer(line):
                            self._add_issue(
                                issues,
                                module,
                                file_name=os.path.basename(file_path),
                                file_line=i+1,
                                description=match.group('description'),
                                issue_kind=issue_kind,
                                size=int(match.group('size')) if match.group('size') else None,
                            )

        return issues

    def _add_issue(self, issues, module, file_name, file_line, description, issue_kind, size):
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

