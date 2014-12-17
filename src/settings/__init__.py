import sys
import imp

try:
    (file, path, description) = imp.find_module('local', __path__)
    if file:
        file.close()
except ImportError:
    print(u"You don't have a settings file in `settings/local.py`")
    print(u"You can use `settings/local.py.example` as a starting point")
    sys.exit(1)

try:
    from .local import INTERNAL_IPS
except ImportError:
    print(u"""
            You must set the INTERNAL_IPS variable. For instance:
            INTERNAL_IPS = ('127.0.0.1',)
         """)
    sys.exit(1)

from .local import *
