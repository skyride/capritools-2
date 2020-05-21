import os

from django.utils.crypto import get_random_string


REDIS_URL = os.environ.get('REDIS_URL')

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.environ.get('SECRET_KEY', get_random_string(12))
DEBUG = bool(int(os.environ.get("DEBUG", False)))

ALLOWED_HOSTS = ["*"]

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', ""),
        'OPTIONS' : {
            'options': os.environ.get('DB_OPTIONS', "")
        }
    },
    # this database should contain a current version of the Static Data Export
    'import': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('SDE_NAME'),
        'USER': os.environ.get('SDE_USER'),
        'PASSWORD': os.environ.get('SDE_PASSWORD'),
        'HOST': os.environ.get('SDE_HOST'),
        'PORT': os.environ.get('SDE_PORT', "")
    },
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': REDIS_URL
    }
}

BROKER_URL = "redis://%s/1" % REDIS_URL
CELERY_RESULT_BACKEND = "redis://%s/2" % REDIS_URL


OLD_SCANS_ROOT = "/old/scans/"
STATIC_ROOT = "/static/"


SOCIAL_AUTH_EVEONLINE_KEY = os.environ.get('SOCIAL_AUTH_KEY')
SOCIAL_AUTH_EVEONLINE_SECRET = os.environ.get('SOCIAL_AUTH_SECRET')
