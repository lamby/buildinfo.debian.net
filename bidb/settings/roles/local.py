import os
from os import environ

from django.utils.log import DEFAULT_LOGGING as LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

DEBUG = True

SITE_URL = environ.get('SITE_URL', 'http://127.0.0.1:8000')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ.get('DB_NAME', 'bidb'),
        'USER': environ.get('DB_USER', 'bidb'),
        'PASSWORD': environ.get('DB_PASSWORD', 'bidb'),
        'HOST': environ.get('DB_HOST', '127.0.0.1'),
        'PORT': environ.get('DB_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
    },
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

BROKER_URL = 'memory://'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

MEDIA_URL = '/storage/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'storage')
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
