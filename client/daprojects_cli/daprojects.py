#!/usr/bin/env python

import argparse

import actions

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
    common_parser.add_argument('-t', '--auth_token',
        type=str,
        help='Authentication API token',
    )

    parser_initialize_project = subparsers.add_parser('initialize_project', aliases=['init'], parents=[common_parser])
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
    parser_initialize_project.add_argument('-i', '--ignore',
        type=str,
        action='append',
        default=[],
        help='Ignore directories that match the pattern (can specify this multiple times)',
    )
    parser_initialize_project.set_defaults(func=actions.initialize_project)

    parser_sync_issues = subparsers.add_parser('sync_issues', aliases=['sync'], parents=[common_parser])
    parser_sync_issues.add_argument('-r', '--source-root',
        type=str,
        default='.',
        help='Root of the source code directory tree',
    )
    parser_sync_issues.set_defaults(func=actions.sync_issues)

    return main_parser


main_parser = define_args()
args = main_parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    print('You need to give a command. Use -h for help.')

