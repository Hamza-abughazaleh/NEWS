"""
Django settings for AswaqCrawling project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
STATIC_ROOT = os.path.join(BASE_DIR, '../statics')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')0yrc(b^u%^_4nk2oyxjpl1%8)2^gxll@1nj6$*9&qhoxi2esf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '40.0.0.131', '127.0.0.1', 'localhost']

# Application definition
LANGUAGE_CODE = 'ar'

LANGUAGES = (
    ('ar', _('Arabic')),
    ('en', _('English')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "News/locale"),
)

LANGUAGE_COOKIE_NAME = 'Newslang'
LANGUAGE_COOKIE_AGE = 31537000

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kombu.transport.django',
    "compressor",
    'djcelery',
    'dynamic_scraper',
    'user',
    'main',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'News.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'main.context_processors.get_websites',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'News.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Crawler',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mydatabase',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

TIME_ZONE = 'Asia/Amman'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
NPM_EXECUTABLE_PATH = 'npm'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder',
    'compressor.finders.CompressorFinder',
)
MEDIA_DIR = os.path.join(BASE_DIR, 'main/media')
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

COMPRESS_PRECOMPILERS = (
    ('text/scss', 'node_modules/node-sass/bin/node-sass {infile} {outfile}'),
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_URL = "/static/"

# django-celery settingscrawling
import djcelery

djcelery.setup_loader()
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_BACKEND = "django"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Celery configuration
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Amman'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

MAX_SPIDER_RUNS_PER_TASK: 10
MAX_CHECKER_RUNS_PER_TASK: 25

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

AUTH_USER_MODEL = 'user.User'

LOGIN_URL = '/user/login/'

LOGIN_REDIRECT_URL = '/user/profile/'
# DEFAULT_FROM_EMAIL = 'noreply@prizila.com'
# # Password Reset Email
# EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
# EMAIL_HOST_USER = 'AKIAIQZXO5TOOOQPROUQ'  # use your gmail
# EMAIL_HOST_PASSWORD = 'ApNbP9P56EQPbaWxvx2oBGG1BeqehKWl16xMOwfpJhZA'  # gmail password
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
