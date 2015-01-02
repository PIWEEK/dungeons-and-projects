import client


def list_projects():
    return client.list_resources(client.base_url + '/projects/')


def retrieve_project(project_url):
    return client.retrieve_resource(project_url)


def list_modules():
    return client.list_resources(client.base_url + '/modules/')


def retrieve_module(module_url):
    return client.retrieve_resource(module_url)


def list_issue_kinds():
    return client.list_resources(client.base_url + '/issue_kinds/')


def retrieve_issue_kind(issue_kind_url):
    return client.retrieve_resource(issue_kind_url)


def list_issues():
    return client.list_resources(client.base_url + '/issues/')


def retrieve_issue(issue_url):
    return client.retrieve_resource(issue_url)

