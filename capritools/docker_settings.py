import os

REDIS_URL = os.environ['REDIS_URL']

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = bool(int(os.environ.get("DEBUG", False)))

ALLOWED_HOSTS = ["*"]

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ.get('DB_PORT', "")
    },
    # this database should contain a current version of the Static Data Export
    'import': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['SDE_NAME'],
        'USER': os.environ['SDE_USER'],
        'PASSWORD': os.environ['SDE_PASSWORD'],
        'HOST': os.environ['SDE_HOST'],
        'PORT': os.environ.get('SDE_PORT', ""),
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


SOCIAL_AUTH_EVEONLINE_KEY = os.environ['SOCIAL_AUTH_KEY']
SOCIAL_AUTH_EVEONLINE_SECRET = os.environ['SOCIAL_AUTH_SECRET']
