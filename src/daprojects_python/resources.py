import client


# Projects

def list_projects():
    return client.list_resources(client.base_url + '/projects/')


def find_project(project_slug):
    projects = client.list_resources(client.base_url + '/projects/?slug={}'.format(project_slug))
    return projects[0] if projects else None


def retrieve_project(project_url):
    return client.retrieve_resource(project_url)


def initialize_project(project_url, tree_structure):
    client.resource_action(project_url + 'initialize/', tree_structure)


def sync_issues(project_url, module_structure):
    client.resource_action(project_url + 'sync_issues/', module_structure)


# Modules

def list_modules():
    return client.list_resources(client.base_url + '/modules/')


def retrieve_module(module_url):
    return client.retrieve_resource(module_url)


# Issue kinds


def list_issue_kinds():
    return client.list_resources(client.base_url + '/issue_kinds/')


def retrieve_issue_kind(issue_kind_url):
    return client.retrieve_resource(issue_kind_url)


# Issues

def list_issues():
    return client.list_resources(client.base_url + '/issues/')


def retrieve_issue(issue_url):
    return client.retrieve_resource(issue_url)


# Directories

def list_directories():
    return client.list_resources(client.base_url + '/directories/')


def retrieve_directory(directory_url):
    return client.retrieve_resource(directory_url)

