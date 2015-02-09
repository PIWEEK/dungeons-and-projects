from daprojects_python import DAProjectsAPI

from code_analyzer import SourceTreeAnalyzer, SourceCodeAnalyzer


def initialize_project(args):
    api = DAProjectsAPI(host_url=args.server, auth_token=args.auth_token)
    project = api.projects.find_by_slug(args.project)
    if project:
        tree_analyzer = SourceTreeAnalyzer(args.source_root, args.depth, args.ignore)
        api.projects.initialize(project.url, tree_analyzer.tree_structure)
        print('Project {} initialized'.format(project.name))
    else:
        print('Cannot found a project with slug {}'.format(args.project))


def sync_issues(args):
    api = DAProjectsAPI(host_url=args.server, auth_token=args.auth_token)
    project = api.projects.find_by_slug(args.project)
    if project:
        code_analyzer = SourceCodeAnalyzer(project, args.source_root, api)
        api.projects.sync_issues(project.url, code_analyzer.module_structure)
        print('Project {} synchronized'.format(project.name))
    else:
        print('Cannot found a project with slug {}'.format(args.project))

