# DEVELOPMENT local settings - add settings_local.py to
# .gitignore so this DOES NOT get checked into version control.

import os
import sys

from os.path import dirname, join
from sys import path

path.append(join(dirname(__file__), "hth"))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

TEMPLATE_DEBUG = True

ADMINS = (
    ('Name Here', 'email@address.tld'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'yourdbname.db'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# development
INTERNAL_IPS = ('127.0.0.1',)

# production - https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-ALLOWED_HOSTS
ALLOWED_HOSTS = ['.domain.tld',]

# development
# Testing Email Sending in local development environment
# https://docs.djangoproject.com/en/dev/topics/email/#testing-e-mail-sending
# http://blog.danawoodman.com/blog/2011/09/11/testing-email-sending-locally-in-django/
# In terminal:
# python -m smtpd -n -c DebuggingServer localhost:1025
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
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mysecrethere-obviously-pick-something-different-and-long-and-complicated-and-do-not-share'