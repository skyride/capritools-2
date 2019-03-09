"""
Django settings for capritools project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i-dna$sritq4-*gm+sk_cx=f9ls1^u$buk+&3g_4__btasieq*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'capritools2',
    'social_django',
]

AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.eveonline.EVEOnlineOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'capritools.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'capritools.wsgi.application'


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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(_PATH, 'static')
STATIC_URL = '/static/'

# ESI
ESI_URL = "https://esi.tech.ccp.is"
ESI_DATASOURCE = "tranquility"
ESI_RETRIES = 15

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_CLEAN_USERNAMES = True
SOCIAL_AUTH_EVEONLINE_SCOPE = [
  "publicData",
  "esi-fleets.read_fleet.v1",
  "esi-fleets.write_fleet.v1"
]

PRICE_URL = "https://api.eve-central.com/api/marketstat/json?regionlimit=10000002&typeid=%s"



# Ship Type Highlighting
DSCAN_HIGHLIGHTS = {
    883: "warning",
    547: "warning",
    906: "info",
    540: "info",
    485: "warning",
    893: "info",
    833: "info",
    894: "info",
    541: "info",
    902: "warning",
    832: "success",
    659: "danger",
    30: "danger",
    1527: "success",
    1534: "info",
    1538: "warning",
    361: "info",
    548: "info",
    1275: "danger",
    1249: "warning"
}

DSCAN_MISC_GROUPS = [548, 361, 1246, 1276, 1275, 1249]

THEMES = [
    "flatly",
    "darkly",
    "cyborg",
    "lumen",
    "slate",
    "solar",
    "yeti"
]

# Celery
CELERY_APP_NAME = "capritools2"
BROKER_URL = "redis://127.0.0.1:6379/"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/"
CELERY_IGNORE_RESULT = False
CELERY_TASK_RESULT_EXPIRES = 1200

CELERY_DISABLE_RATE_LIMITS = True
CELERYD_TASK_SOFT_TIME_LIMIT = 300
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

# Periodic tasks
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    # Spawns market update tasks
    'price_update_spawner': {
        'task': 'price_update_spawner',
        'schedule': timedelta(minutes=2)
    },
    'fetch_spawner': {
        'task': 'fetch_spawner',
        'schedule': timedelta(minutes=1)
    },
    'fleet_live_update_spawner': {
        'task': 'fleet_live_update_spawner',
        'schedule': timedelta(seconds=10)
    }
}

# load local settings
from local_settings import *  # NOPEP8