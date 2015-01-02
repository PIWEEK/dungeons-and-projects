import client


class Project(client.Resource):
    pass


def list_projects():
    return client.list_resources(client.base_url + '/projects/', Project)


def retrieve_project(project_url):
    return client.retrieve_resource(project_url, Project)


class Module(client.Resource):
    pass


def list_modules():
    return client.list_resources(client.base_url + '/modules/', Module)


def retrieve_module(module_url):
    return client.retrieve_resource(module_url, Module)

