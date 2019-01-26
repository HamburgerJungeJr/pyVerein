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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = os.environ['STATIC_URL']

MEDIA_URL = os.environ['MEDIA_URL']
MEDIA_ROOT = os.environ['MEDIA_ROOT']

SENDFILE_URL = os.environ['SENDFILE_URL']
SENDFILE_ROOT = os.environ['SENDFILE_ROOT']
SENDFILE_BACKEND = 'sendfile.backends.development'