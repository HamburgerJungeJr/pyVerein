"""
Django settings for pyVerein project.
This settings are used in production environment.
"""
from pyVerein.settings.base import *

import dj_database_url

STATIC_ROOT = os.environ['STATIC_ROOT']

ALLOWED_HOSTS = [os.environ['DJANGO_PROD_HOST']]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = os.environ['STATIC_URL']

MEDIA_URL = os.environ['MEDIA_URL']
MEDIA_ROOT = os.environ['MEDIA_ROOT']

SENDFILE_URL = os.environ['SENDFILE_URL']
SENDFILE_ROOT = os.environ['SENDFILE_ROOT']
SENDFILE_BACKEND = os.environ['SENDFILE_BACKEND']