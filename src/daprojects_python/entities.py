import client


class Project(client.Entity):
    pass


def list_projects():
    return client.list_entities(client.base_url + '/projects/', Project)


def retrieve_project(project_url):
    return client.retrieve_entity(project_url, Project)

