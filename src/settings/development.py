"""
Default Django settings for a development environment.
"""

from .common import *

INSTALLED_APPS += (
    'django_extensions',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = ('127.0.0.1',)

