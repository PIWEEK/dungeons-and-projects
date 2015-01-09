import requests


class Resource:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


base_url = 'http://localhost:8000/api/v1'


def set_host(host_url):
    global base_url
    base_url = host_url + '/api/v1'


def list_resources(resource_url, resource_class=Resource):
    response = requests.get(resource_url)
    response.raise_for_status()
    return [resource_class(**resource_data) for resource_data in response.json()]


def retrieve_resource(resource_url, resource_class=Resource):
    response = requests.get(resource_url)
    response.raise_for_status()
    return resource_class(**response.json())


def resource_action(action_url, action_data):
    response = requests.post(action_url, data=action_data)
    response.raise_for_status()
    return response.json()

