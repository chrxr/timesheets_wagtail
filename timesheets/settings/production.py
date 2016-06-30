from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*', 'timesheets-qa.bodleian.ox.ac.uk', 'localhost']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
    	'file': {
    		'level': 'DEBUG',
    		'class': 'logging.FileHandler',
    		'filename': BASE_DIR + '/debug.log',
    	},
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
