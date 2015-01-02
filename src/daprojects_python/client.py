import requests


class Entity:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


base_url = 'http://localhost:8000/api/v1'


def set_host(host_url):
    global base_url
    base_url = host_url + '/api/v1'


def list_entities(resource_url, entity_class=Entity):
    response = requests.get(resource_url)
    response.raise_for_status()
    return [entity_class(**entity_data) for entity_data in response.json()]


def retrieve_entity(entity_url, entity_class=Entity):
    response = requests.get(entity_url)
    response.raise_for_status()
    return entity_class(**response.json())

