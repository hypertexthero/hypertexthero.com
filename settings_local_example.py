# DEVELOPMENT local settings - add settings_local.py to
# .gitignore so this DOES NOT get checked into version control.

import os
import sys

from os.path import dirname, join
from sys import path

path.append(join(dirname(__file__), "hth"))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# change to False for production
DEBUG = True

# change to False for production
TEMPLATE_DEBUG = True

ADMINS = (
    ('Name Here', 'email@address.tld'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, '..', 'yourdbname.db'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# important to set this correctly for persona authentication!
# http://django-browserid.readthedocs.org/en/v0.9/setup.html#installation
# =Mozilla =Persona
SITE_URL = 'http://127.0.0.1:8000'
BROWSERID_CREATE_USER = False
# Path to redirect to on successful login.
LOGIN_REDIRECT_URL = '/'
# Path to redirect to on unsuccessful login attempt.
LOGIN_REDIRECT_URL_FAILURE = '/'
# Path to redirect to on logout.
LOGOUT_REDIRECT_URL = '/'

# development - uncomment 2 lines below
# INTERNAL_IPS = ('127.0.0.1',)
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# production - uncomment line below # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-ALLOWED_HOSTS
# ALLOWED_HOSTS = ['.domain.tld',]

# development email
# Testing Email Sending in local development environment
# https://docs.djangoproject.com/en/dev/topics/email/#testing-e-mail-sending
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = "localhost"
# EMAIL_PORT = 1025

# production email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = "localhost"
EMAIL_PORT = 587

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "static/files")

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://domain.tld/static/files/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://domain.tld/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = os.path.join(PROJECT_ROOT, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mysecrethere-obviously-pick-something-different-and-long-and-complicated-and-do-not-share'