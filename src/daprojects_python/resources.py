import client


class Project(client.Resource):
    pass


def list_projects():
    return client.list_resources(client.base_url + '/projects/', Project)


def retrieve_project(project_url):
    return client.retrieve_resource(project_url, Project)

