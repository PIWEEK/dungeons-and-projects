#!/usr/bin/env python

import argparse

from daprojects_python import client, resources

import code_analyzer

def define_args():
    main_parser = argparse.ArgumentParser(
        description='''
        Command line client for Dungeons & Projects application. You can interactively
        browse a project, or automatically configure it.
        ''',
    )
    subparsers = main_parser.add_subparsers(
        title='Commands',
        description='Choose what to execute (COMMAND -h for further help)',
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('project',
        type=str,
        help='Slug of the project in the server',
    )
    common_parser.add_argument('-s', '--server',
        type=str,
        help='HTTP address of the server (by default http://localhost:8000)',
    )

    parser_initialize_project = subparsers.add_parser('initialize_project', parents=[common_parser])
    parser_initialize_project.add_argument('-r', '--source-root',
        type=str,
        default='.',
        help='Root of the source code directory tree',
    )
    parser_initialize_project.add_argument('-d', '--depth',
        type=int,
        default=3,
        help='Number of tree levels to analyze (by default 3)',
    )
    parser_initialize_project.set_defaults(func=initialize_project)

    parser_sync_issues = subparsers.add_parser('sync_issues', parents=[common_parser])
    parser_sync_issues.add_argument('-r', '--source-root',
        type=str,
        default='.',
        help='Root of the source code directory tree',
    )
    parser_sync_issues.set_defaults(func=sync_issues)

    return main_parser


def initialize_project(args):
    if args.server:
        client.set_host(args.server)
    project = resources.find_project(args.project)
    if project:
        tree_structure = code_analyzer.read_tree_structure(args.source_root, args.depth)
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


main_parser = define_args()
args = main_parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    print('You need to give a command. Use -h for help.')

