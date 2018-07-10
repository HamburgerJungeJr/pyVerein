"""
Django settings for pyVerein project.
This settings are used in development environment.
"""
from pyVerein.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STATICFILES_DIRS = [
    '../static/',
]

# Debug Toolbar
INSTALLED_APPS += [
    
]
MIDDLEWARE += [
    
]
INTERNAL_IPS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}