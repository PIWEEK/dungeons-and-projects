import unittest
from unittest.mock import Mock, patch
from collections import namedtuple
from requests import exceptions

from client import DAPClient


class TestDAPCLient(unittest.TestCase):

    def test_set_base_url(self):
        client = DAPClient('https://example.com:9090')

        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = []
            mock_requests_get.return_value = mock_response

            projects = client.list_projects()

            mock_requests_get.assert_called_once_with('https://example.com:9090/api/v1/projects/')
            self.assertEqual(len(projects), 0)

    def test_error_checking(self):
        client = DAPClient()

        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = exceptions.RequestException('Not Found')
            mock_requests_get.return_value = mock_response

            with self.assertRaises(exceptions.RequestException):
                projects = client.list_projects()

            mock_response.raise_for_status.assert_called_once()

    def test_list_projects(self):
        client = DAPClient()

        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    "url": "http://localhost:8000/api/v1/projects/1",
                    "name": "Test Project 1",
                    "slug": "test-project-1",
                    "description": "Test description 1"
                },
                {
                    "url": "http://localhost:8000/api/v1/projects/2",
                    "name": "Test Project 2",
                    "slug": "test-project-2",
                    "description": "Test description 2"
                }
            ]
            mock_requests_get.return_value = mock_response

            projects = client.list_projects()

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/projects/')

            self.assertEqual(len(projects), 2)
            self.assertEqual(projects[0].url, 'http://localhost:8000/api/v1/projects/1')
            self.assertEqual(projects[0].name, 'Test Project 1')
            self.assertEqual(projects[0].slug, 'test-project-1')
            self.assertEqual(projects[0].description, 'Test description 1')
            self.assertEqual(projects[1].url, 'http://localhost:8000/api/v1/projects/2')
            self.assertEqual(projects[1].name, 'Test Project 2')
            self.assertEqual(projects[1].slug, 'test-project-2')
            self.assertEqual(projects[1].description, 'Test description 2')

    def test_retrieve_project(self):
        client = DAPClient()

        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "url": "http://localhost:8000/api/v1/projects/1",
                "name": "Test Project",
                "slug": "test-project",
                "description": "Test description"
            }
            mock_requests_get.return_value = mock_response

            project = client.retrieve_project("http://localhost:8000/api/v1/projects/1")

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/projects/1')

            self.assertEqual(project.url, 'http://localhost:8000/api/v1/projects/1')
            self.assertEqual(project.name, 'Test Project')
            self.assertEqual(project.slug, 'test-project')
            self.assertEqual(project.description, 'Test description')

