from .base import *

DEBUG = True

import os
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ALLOWED_HOSTS = [
    "*",
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

API_KEY = os.getenv("API_KEY")

CSRF_TRUSTED_ORIGINS = [
    "https://example.com"
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('PGDATABASE'),
        'USER': env('PGUSER'),
        'PASSWORD': env('PGPASSWORD'),
        'HOST': env('PGHOST', default='localhost'),
        'PORT': env('PGPORT', default='5432'),
    }
}

# Cache settings
# https://docs.djangoproject.com/en/5.0/topics/cache/#setting-up-the-cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# local.py - local development settings Without modifying the base.py file, you can create a local.py file in the
# same directory as settings.py and add the following code:
# try:
#     from .local import *
# except ImportError:
#     pass
