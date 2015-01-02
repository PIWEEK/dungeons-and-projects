import requests

import entities

class RESTClient:

    def __init__(self, host_url='http://localhost:8000'):
        self.base_url = host_url + '/api/v1'

    def _list_entities(self, resource_url, entity_class):
        response = requests.get(resource_url)
        response.raise_for_status()
        return [entity_class(**entity_data) for entity_data in response.json()]

    def _retrieve_entity(self, entity_url, entity_class):
        response = requests.get(entity_url)
        response.raise_for_status()
        return entity_class(**response.json())


class DAPClient(RESTClient):

    def list_projects(self):
        return self._list_entities(self.base_url + '/projects/', entities.Project)

    def retrieve_project(self, project_url):
        return self._retrieve_entity(project_url, entities.Project)

