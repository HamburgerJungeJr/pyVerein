"""
Django settings for pyVerein project.
This settings are used in production environment.
"""
from pyVerein.settings.base import *

import dj_database_url

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

ALLOWED_HOSTS = [os.environ['DJANGO_PROD_HOST']]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}