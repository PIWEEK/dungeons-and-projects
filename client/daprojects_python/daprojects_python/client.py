import requests
import json


class APIResource:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class APIResourceList:
    resource_class = APIResource  # MAY redefine in subclasses
    resource_path = None          # MUST redefine in subclasses

    def __init__(self, client):
        self._client = client

    def _list_url(self):
        return self._client.base_url + self.resource_path

    def _list(self, filters={}):
        return self._client.list_resources(self._list_url(), self.resource_class, filters)

    def _find_one(self, filters={}):
        resources = self._client.list_resources(self._list_url(), self.resource_class, filters)
        return resources[0] if resources else None

    def _retrieve(self, resource_url):
        return self._client.retrieve_resource(resource_url, self.resource_class)

    def _list_action(self, action_name, action_data):
        return self._client.resource_action(self._list_url() + action_name, action_data)

    def _resource_action(self, resource_url, action_name, action_data):
        return self._client.resource_action(resource_url + action_name, action_data)


class APIClient:
    def __init__(self, host_url=None, auth_token=None):
        if not host_url:
            host_url = 'http://localhost:8000'
        if not host_url.startswith('http'):
            host_url = 'http://' + host_url
        self.base_url = host_url.lower().strip() + '/api/v1'
        if not auth_token:
            auth_token = ''
        self.auth_token = auth_token

    def list_resources(self, resource_url, resource_class, filters={}):
        response = requests.get(
            resource_url,
            params=filters,
            headers={'Authorization': 'Token {}'.format(self.auth_token)}
        )
        response.raise_for_status()
        return [resource_class(**resource_data) for resource_data in response.json()]

    def retrieve_resource(self, resource_url, resource_class):
        response = requests.get(
            resource_url,
            headers={'Authorization': 'Token {}'.format(self.auth_token)}
        )
        response.raise_for_status()
        return resource_class(**response.json())

    def resource_action(self, action_url, action_data):
        response = requests.post(
            action_url,
            data=json.dumps(action_data),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Token {}'.format(self.auth_token)
            }
        )
        response.raise_for_status()
        return response.json()

