import requests
import json


class Resource:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


base_url = 'http://localhost:8000/api/v1'
auth_token = ''


def set_host(host_url):
    global base_url
    base_url = host_url.lower().strip() + '/api/v1'
    if not base_url.startswith('http'):
        base_url = 'http://' + base_url


def set_auth_token(token):
    global auth_token
    auth_token = token


def list_resources(resource_url, resource_class=Resource):
    response = requests.get(
        resource_url,
        headers={'Authorization': 'Token {}'.format(auth_token)}
    )
    response.raise_for_status()
    return [resource_class(**resource_data) for resource_data in response.json()]


def retrieve_resource(resource_url, resource_class=Resource):
    response = requests.get(
        resource_url,
        headers={'Authorization': 'Token {}'.format(auth_token)}
    )
    response.raise_for_status()
    return resource_class(**response.json())


def resource_action(action_url, action_data):
    response = requests.post(
        action_url,
        data=json.dumps(action_data),
        headers={'content-type': 'application/json', 'Authorization': 'Token {}'.format(auth_token)}
    )
    response.raise_for_status()
    return response.json()

