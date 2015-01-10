from django.conf.urls import patterns, include, url
from django.contrib import admin

from daprojects_api import urls as urls_api

from .views import *

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^project/(?P<project_id>\d+)/$', ProjectView.as_view(), name='project'),
    url(r'^project/(?P<project_id>\d+)/module/(?P<module_id>\d+)/$', ModuleView.as_view(), name='module'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include(urls_api)),
)

