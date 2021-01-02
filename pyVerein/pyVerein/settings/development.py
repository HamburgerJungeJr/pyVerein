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

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SENDFILE_URL = '/sendfile/'
SENDFILE_ROOT = os.path.join(BASE_DIR, 'sendfile')
SENDFILE_BACKEND = 'sendfile.backends.development'
