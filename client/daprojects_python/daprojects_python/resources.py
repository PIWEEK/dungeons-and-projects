
from .client import APIClient, APIResourceList, APIResource

class DAProjectsAPI():

    def __init__(self, *args, **kwargs):
        client = APIClient(*args, **kwargs)
        self.projects = Projects(client)
        self.modules = Modules(client)
        self.issue_kinds = IssueKinds(client)
        self.issues = Issues(client)
        self.directories = Directories(client)


class Projects(APIResourceList):
    resource_path = '/projects/'

    def list(self):
        return self._list()

    def find_by_slug(self, project_slug):
        return self._find_one({'slug': project_slug})

    def retrieve(self, project_url):
        return self._retrieve(project_url)

    def initialize(self, project_url, tree_structure):
        return self._resource_action(project_url, 'initialize/', tree_structure)

    def sync_issues(self, project_url, module_structure):
        return self._resource_action(project_url, 'sync_issues/', module_structure)


class Modules(APIResourceList):
    resource_path = '/modules/'

    def list(self):
        return self._list()

    def retrieve(self, module_url):
        return self._retrieve(module_url)


class IssueKinds(APIResourceList):
    resource_path = '/issue_kinds/'

    def list(self):
        return self._list()

    def retrieve(self, issue_kind_url):
        return self._retrieve(issue_kind_url)


class Issues(APIResourceList):
    resource_path = '/issues/'

    def list(self):
        return self._list()

    def retrieve(self, issue_url):
        return self._retrieve(issue_url)


class Directories(APIResourceList):
    resource_path = '/directories/'

    def list(self):
        return self._list()

    def retrieve(self, directory_url):
        return self._retrieve(directory_url)

