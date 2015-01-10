import unittest
from unittest.mock import Mock, patch
from collections import namedtuple
from requests import exceptions

import client
import resources


class TestClient(unittest.TestCase):

    def test_set_base_url(self):
        client.set_host('https://example.com:9090')

        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = []
            mock_requests_get.return_value = mock_response

            some_resources = client.list_resources(client.base_url + '/some_resources/')

            mock_requests_get.assert_called_once_with('https://example.com:9090/api/v1/some_resources/')
            self.assertEqual(len(some_resources), 0)

        client.set_host('http://localhost:8000')

    def test_error_checking(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = exceptions.RequestException('Not Found')
            mock_requests_get.return_value = mock_response

            with self.assertRaises(exceptions.RequestException):
                some_resources = client.list_resources(client.base_url + '/some_resources/')

            mock_response.raise_for_status.assert_called_once()

    def test_resource_subclass(self):

        class SomeResource(client.Resource):
            def some_method(self):
                return self.a + self.b

        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "url": 'http://localhost:8000/api/v1/some_resources/1/',
                "a": 66,
                "b": 99,
            }
            mock_requests_get.return_value = mock_response

            some_resource = client.retrieve_resource(client.base_url + '/some_resources/1/', SomeResource)

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/some_resources/1/')
            self.assertTrue(isinstance(some_resource, SomeResource))
            self.assertEqual(some_resource.some_method(), 66 + 99)


class TestProjects(unittest.TestCase):

    def test_list_projects(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                self._sample_project(1),
                self._sample_project(2)
            ]
            mock_requests_get.return_value = mock_response

            projects = resources.list_projects()

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/projects/')

            self.assertEqual(len(projects), 2)
            self.assertEqual(projects[0].url, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(projects[0].name, 'Test Project 1')
            self.assertEqual(projects[0].slug, 'test-project-1')
            self.assertEqual(projects[0].description, 'Project description 1')
            self.assertEqual(projects[1].url, 'http://localhost:8000/api/v1/projects/2/')
            self.assertEqual(projects[1].name, 'Test Project 2')
            self.assertEqual(projects[1].slug, 'test-project-2')
            self.assertEqual(projects[1].description, 'Project description 2')

    def test_find_project(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = [self._sample_project(1)]
            mock_requests_get.return_value = mock_response

            project = resources.find_project("test-project-1")

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/projects/?slug=test-project-1')

            self.assertEqual(project.url, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(project.name, 'Test Project 1')
            self.assertEqual(project.slug, 'test-project-1')
            self.assertEqual(project.description, 'Project description 1')

    def test_retrieve_project(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = self._sample_project(1)
            mock_requests_get.return_value = mock_response

            project = resources.retrieve_project("http://localhost:8000/api/v1/projects/1/")

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/projects/1/')

            self.assertEqual(project.url, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(project.name, 'Test Project 1')
            self.assertEqual(project.slug, 'test-project-1')
            self.assertEqual(project.description, 'Project description 1')

    def test_initialize_project(self):
        with patch('client.requests.post') as mock_requests_post:
            mock_response = Mock()
            mock_response.json.return_value = '{"status": "Project initialized"}'
            mock_requests_post.return_value = mock_response

            tree_structure = """
            [
                {
                    "name": "dir-1",
                    "subdirs" [
                        {
                            "name": "dir-1-1",
                            "subdirs": []
                        },
                        {
                            "name": "dir-1-2",
                            "subdirs": []
                        }
                    ]
                },
                {
                    "name": "dir-2",
                    "subdirs": []
                }
            ]
            """
            resources.initialize_project("http://localhost:8000/api/v1/projects/1/", tree_structure)

            mock_requests_post.assert_called_once_with(
                'http://localhost:8000/api/v1/projects/1/initialize/',
                data=tree_structure
            )

    def test_sync_issues(self):
        with patch('client.requests.post') as mock_requests_post:
            mock_response = Mock()
            mock_response.json.return_value = '{"status": "Project synchronized"}'
            mock_requests_post.return_value = mock_response

            module_structure = """
            [
                {
                    "module": "http://localhost:8000/api/v1/modules/1/",
                    "issues": [
                        {
                            "file_name": "some_file_1.py",
                            "file_line": null,
                            "description": "this is one TODO",
                            "kind": "http://localhost:8000/api/v1/issue_kinds/2",
                            "size": 3
                        },
                        {
                            "file_name": "some_file_2.py",
                            "file_line": 33,
                            "description": "this is other TODO",
                            "kind": "http://localhost:8000/api/v1/issue_kinds/3",
                            "size": 5
                        }
                    ]
                    "submodules" [
                        {
                            "module": "http://localhost:8000/api/v1/modules/2/",
                            "issues": []
                            "submodules": []
                        },
                        {
                            "module": "http://localhost:8000/api/v1/modules/3/",
                            "issues": []
                            "submodules": []
                        }
                    ]
                },
                {
                    {
                        "module": "http://localhost:8000/api/v1/modules/4/",
                        "issues": []
                        "submodules": []
                    }
                }
            ]
            """
            resources.sync_issues("http://localhost:8000/api/v1/projects/1/", module_structure)

            mock_requests_post.assert_called_once_with(
                'http://localhost:8000/api/v1/projects/1/sync_issues/',
                data=module_structure
            )

    def _sample_project(self, project_id):
        return {
            "url": "http://localhost:8000/api/v1/projects/{}/".format(project_id),
            "name": "Test Project {}".format(project_id),
            "slug": "test-project-{}".format(project_id),
            "description": "Project description {}".format(project_id),
        }


class TestModules(unittest.TestCase):

    def test_list_modules(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                self._sample_module(1),
                self._sample_module(2),
            ]
            mock_requests_get.return_value = mock_response

            modules = resources.list_modules()

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/modules/')

            self.assertEqual(len(modules), 2)
            self.assertEqual(modules[0].url, 'http://localhost:8000/api/v1/modules/1/')
            self.assertEqual(modules[0].project, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(modules[0].parent, None)
            self.assertEqual(modules[0].children, [])
            self.assertEqual(modules[0].name, 'Test Module 1')
            self.assertEqual(modules[0].slug, 'test-module-1')
            self.assertEqual(modules[0].description, 'Module description 1')
            self.assertEqual(modules[0].directories, [])
            self.assertEqual(modules[0].issues, [])
            self.assertEqual(modules[1].url, 'http://localhost:8000/api/v1/modules/2/')
            self.assertEqual(modules[1].project, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(modules[1].parent, None)
            self.assertEqual(modules[1].children, [])
            self.assertEqual(modules[1].name, 'Test Module 2')
            self.assertEqual(modules[1].slug, 'test-module-2')
            self.assertEqual(modules[1].description, 'Module description 2')
            self.assertEqual(modules[1].directories, [])
            self.assertEqual(modules[1].issues, [])

    def test_retrieve_module(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = self._sample_module(1)
            mock_requests_get.return_value = mock_response

            module = resources.retrieve_module("http://localhost:8000/api/v1/modules/1/")

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/modules/1/')

            self.assertEqual(module.url, 'http://localhost:8000/api/v1/modules/1/')
            self.assertEqual(module.project, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(module.parent, None)
            self.assertEqual(module.children, [])
            self.assertEqual(module.name, 'Test Module 1')
            self.assertEqual(module.slug, 'test-module-1')
            self.assertEqual(module.description, 'Module description 1')
            self.assertEqual(module.directories, [])
            self.assertEqual(module.issues, [])

    def test_module_project(self):
        module = client.Resource(**self._sample_module(1, project_id=1))
        self.assertEqual(module.project, 'http://localhost:8000/api/v1/projects/1/')

    def test_module_parent(self):
        module = client.Resource(**self._sample_module(2, parent_id=1))
        self.assertEqual(module.parent, 'http://localhost:8000/api/v1/modules/1/')

    def test_module_children(self):
        module = client.Resource(**self._sample_module(1, child_ids=[2, 3, 4]))
        for i, child_id in enumerate([2, 3, 4]):
            self.assertEqual(module.children[i], 'http://localhost:8000/api/v1/modules/{}/'.format(child_id))

    def test_module_directories(self):
        module = client.Resource(**self._sample_module(1, directory_ids=[2, 3, 4]))
        for i, directory_id in enumerate([2, 3, 4]):
            self.assertEqual(module.directories[i], 'http://localhost:8000/api/v1/directories/{}/'.format(directory_id))

    def test_module_issues(self):
        module = client.Resource(**self._sample_module(1, issue_ids=[2, 3, 4]))
        for i, issue_id in enumerate([2, 3, 4]):
            self.assertEqual(module.issues[i], 'http://localhost:8000/api/v1/issues/{}/'.format(issue_id))

    def _sample_module(self, module_id, project_id=1, parent_id=None, child_ids=[], directory_ids=[], issue_ids=[]):
        return {
            "url": "http://localhost:8000/api/v1/modules/{}/".format(module_id),
            "project": "http://localhost:8000/api/v1/projects/{}/".format(project_id),
            "parent": "http://localhost:8000/api/v1/modules/{}/".format(parent_id) if parent_id else None,
            "children": ["http://localhost:8000/api/v1/modules/{}/".format(child_id) for child_id in child_ids],
            "name": "Test Module {}".format(module_id),
            "slug": "test-module-{}".format(module_id),
            "description": "Module description {}".format(module_id),
            "directories": ["http://localhost:8000/api/v1/directories/{}/".format(directory_id) for directory_id in directory_ids],
            "issues": ["http://localhost:8000/api/v1/issues/{}/".format(issue_id) for issue_id in issue_ids],
        }


class TestIssueKinds(unittest.TestCase):

    def test_list_issue_kinds(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                self._sample_issue_kind(1),
                self._sample_issue_kind(2)
            ]
            mock_requests_get.return_value = mock_response

            issue_kinds = resources.list_issue_kinds()

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/issue_kinds/')

            self.assertEqual(len(issue_kinds), 2)
            self.assertEqual(issue_kinds[0].url, 'http://localhost:8000/api/v1/issue_kinds/1/')
            self.assertEqual(issue_kinds[0].name, 'Test IssueKind 1')
            self.assertEqual(issue_kinds[1].url, 'http://localhost:8000/api/v1/issue_kinds/2/')
            self.assertEqual(issue_kinds[1].name, 'Test IssueKind 2')

    def test_retrieve_issue_kind(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = self._sample_issue_kind(1)
            mock_requests_get.return_value = mock_response

            issue_kind = resources.retrieve_issue_kind("http://localhost:8000/api/v1/issue_kinds/1/")

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/issue_kinds/1/')

            self.assertEqual(issue_kind.url, 'http://localhost:8000/api/v1/issue_kinds/1/')
            self.assertEqual(issue_kind.name, 'Test IssueKind 1')

    def _sample_issue_kind(self, issue_kind_id):
        return {
            "url": "http://localhost:8000/api/v1/issue_kinds/{}/".format(issue_kind_id),
            "name": "Test IssueKind {}".format(issue_kind_id),
        }


class TestIssues(unittest.TestCase):

    def test_list_issues(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                self._sample_issue(1),
                self._sample_issue(2)
            ]
            mock_requests_get.return_value = mock_response

            issues = resources.list_issues()

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/issues/')

            self.assertEqual(len(issues), 2)
            self.assertEqual(issues[0].url, 'http://localhost:8000/api/v1/issues/1/')
            self.assertEqual(issues[0].module, 'http://localhost:8000/api/v1/modules/1/')
            self.assertEqual(issues[0].name, 'Test Issue 1')
            self.assertEqual(issues[0].file_name, 'file-name-1.py')
            self.assertEqual(issues[0].file_line, 667)
            self.assertEqual(issues[0].kind, 'http://localhost:8000/api/v1/issue_kinds/1/')
            self.assertEqual(issues[0].size, 1000)
            self.assertEqual(issues[0].description, 'Issue description 1')
            self.assertEqual(issues[1].url, 'http://localhost:8000/api/v1/issues/2/')
            self.assertEqual(issues[1].module, 'http://localhost:8000/api/v1/modules/1/')
            self.assertEqual(issues[1].name, 'Test Issue 2')
            self.assertEqual(issues[1].file_name, 'file-name-2.py')
            self.assertEqual(issues[1].file_line, 668)
            self.assertEqual(issues[1].kind, 'http://localhost:8000/api/v1/issue_kinds/1/')
            self.assertEqual(issues[1].size, 1001)
            self.assertEqual(issues[1].description, 'Issue description 2')

    def test_retrieve_issue(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = self._sample_issue(1)
            mock_requests_get.return_value = mock_response

            issue = resources.retrieve_issue("http://localhost:8000/api/v1/issues/1/")

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/issues/1/')

            self.assertEqual(issue.url, 'http://localhost:8000/api/v1/issues/1/')
            self.assertEqual(issue.module, 'http://localhost:8000/api/v1/modules/1/')
            self.assertEqual(issue.name, 'Test Issue 1')
            self.assertEqual(issue.file_name, 'file-name-1.py')
            self.assertEqual(issue.file_line, 667)
            self.assertEqual(issue.kind, 'http://localhost:8000/api/v1/issue_kinds/1/')
            self.assertEqual(issue.size, 1000)
            self.assertEqual(issue.description, 'Issue description 1')

    def test_issue_module(self):
        issue = client.Resource(**self._sample_issue(1, module_id=1))
        self.assertEqual(issue.module, 'http://localhost:8000/api/v1/modules/1/')

    def test_issue_issue_kind(self):
        issue = client.Resource(**self._sample_issue(1, issue_kind_id=1))
        self.assertEqual(issue.kind, 'http://localhost:8000/api/v1/issue_kinds/1/')

    def _sample_issue(self, issue_id, module_id=1, issue_kind_id=1):
        return {
            "url": "http://localhost:8000/api/v1/issues/{}/".format(issue_id),
            "module": "http://localhost:8000/api/v1/modules/{}/".format(module_id),
            "name": "Test Issue {}".format(issue_id),
            "file_name": "file-name-{}.py".format(issue_id),
            "file_line": 666 + issue_id,
            "description": "Issue description {}".format(issue_id),
            "kind": "http://localhost:8000/api/v1/issue_kinds/{}/".format(issue_kind_id),
            "size": 999 + issue_id,
        }


class TestDirectories(unittest.TestCase):

    def test_list_directories(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                self._sample_directory(1),
                self._sample_directory(2),
            ]
            mock_requests_get.return_value = mock_response

            directories = resources.list_directories()

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/directories/')

            self.assertEqual(len(directories), 2)
            self.assertEqual(directories[0].url, 'http://localhost:8000/api/v1/directories/1/')
            self.assertEqual(directories[0].project, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(directories[0].parent, None)
            self.assertEqual(directories[0].children, [])
            self.assertEqual(directories[0].slug, 'test-directory-1')
            self.assertEqual(directories[0].modules, [])
            self.assertEqual(directories[1].url, 'http://localhost:8000/api/v1/directories/2/')
            self.assertEqual(directories[1].project, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(directories[1].parent, None)
            self.assertEqual(directories[1].children, [])
            self.assertEqual(directories[1].slug, 'test-directory-2')
            self.assertEqual(directories[1].modules, [])

    def test_retrieve_directory(self):
        with patch('client.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = self._sample_directory(1)
            mock_requests_get.return_value = mock_response

            directory = resources.retrieve_directory("http://localhost:8000/api/v1/directories/1/")

            mock_requests_get.assert_called_once_with('http://localhost:8000/api/v1/directories/1/')

            self.assertEqual(directory.url, 'http://localhost:8000/api/v1/directories/1/')
            self.assertEqual(directory.project, 'http://localhost:8000/api/v1/projects/1/')
            self.assertEqual(directory.parent, None)
            self.assertEqual(directory.children, [])
            self.assertEqual(directory.slug, 'test-directory-1')
            self.assertEqual(directory.modules, [])

    def test_directory_project(self):
        directory = client.Resource(**self._sample_directory(1, project_id=1))
        self.assertEqual(directory.project, 'http://localhost:8000/api/v1/projects/1/')

    def test_directory_parent(self):
        directory = client.Resource(**self._sample_directory(2, parent_id=1))
        self.assertEqual(directory.parent, 'http://localhost:8000/api/v1/directories/1/')

    def test_directory_children(self):
        directory = client.Resource(**self._sample_directory(1, child_ids=[2, 3, 4]))
        for i, child_id in enumerate([2, 3, 4]):
            self.assertEqual(directory.children[i], 'http://localhost:8000/api/v1/directories/{}/'.format(child_id))

    def test_directory_modules(self):
        directory = client.Resource(**self._sample_directory(1, module_ids=[2, 3, 4]))
        for i, module_id in enumerate([2, 3, 4]):
            self.assertEqual(directory.modules[i], 'http://localhost:8000/api/v1/modules/{}/'.format(module_id))

    def _sample_directory(self, directory_id, project_id=1, parent_id=None, child_ids=[], module_ids=[]):
        return {
            "url": "http://localhost:8000/api/v1/directories/{}/".format(directory_id),
            "project": "http://localhost:8000/api/v1/projects/{}/".format(project_id),
            "parent": "http://localhost:8000/api/v1/directories/{}/".format(parent_id) if parent_id else None,
            "children": ["http://localhost:8000/api/v1/directories/{}/".format(child_id) for child_id in child_ids],
            "slug": "test-directory-{}".format(directory_id),
            "modules": ["http://localhost:8000/api/v1/modules/{}/".format(module_id) for module_id in module_ids],
        }

