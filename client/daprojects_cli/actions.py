from daprojects_python import client, resources

import code_analyzer


def initialize_project(args):
    if args.server:
        client.set_host(args.server)
    project = resources.find_project(args.project)
    if project:
        tree_structure = code_analyzer.read_tree_structure(args.source_root, args.depth, args.ignore)
        resources.initialize_project(project.url, tree_structure)
        print('Project {} initialized'.format(project.name))
    else:
        print('Cannot found a project with slug {}'.format(args.project))


def sync_issues(args):
    if args.server:
        client.set_host(args.server)
    project = resources.find_project(args.project)
    if project:
        module_structure = code_analyzer.find_module_issues(project, args.source_root)
        resources.sync_issues(project.url, module_structure)
        print('Project {} synchronized'.format(project.name))
    else:
        print('Cannot found a project with slug {}'.format(args.project))

