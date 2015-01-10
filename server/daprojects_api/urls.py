from django.conf.urls import url, include
from rest_framework import routers

from .views import ProjectViewSet, ModuleViewSet, IssueKindViewSet, IssueViewSet, DirectoryViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'issue_kinds', IssueKindViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'directories', DirectoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

