from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['chrxr.com']

try:
    from .local import *
except ImportError:
    pass
