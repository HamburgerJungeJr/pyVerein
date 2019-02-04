"""
Django settings for pyVerein project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.environ['SECRET_KEY']

# Application definition

INSTALLED_APPS = [
    'custom_translations.apps.CustomTranslationsConfig',
    'account.apps.AccountConfig',
    'app.apps.AppConfig',
    'members.apps.MembersConfig',
    'finance.apps.FinanceConfig',
    'reporting.apps.ReportingConfig',
    'tasks.apps.TasksConfig',
    'utils.apps.UtilsConfig',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',
    'dynamic_preferences',
    'author',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = 'pyVerein.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dynamic_preferences.processors.global_preferences',
            ],
        },
    },
]

WSGI_APPLICATION = 'pyVerein.wsgi.application'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German'))
)


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = 'app:index'
LOGOUT_REDIRECT_URL = 'account:login'

AUTHOR_CREATED_BY_FIELD_NAME = 'created_by'
AUTHOR_UPDATED_BY_FIELD_NAME = 'last_modified_by'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTH_USER_MODEL = 'account.User'