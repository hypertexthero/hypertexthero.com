# DEVELOPMENT local settings - add settings_local.py to
# .gitignore so this DOES NOT get checked into version control.


DEBUG = True

TEMPLATE_DEBUG = True

ADMINS = (
    ('Name Here', 'email@address.tld'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INTERNAL_IPS = ('127.0.0.1',)

# Testing Email Sending in local development environment
# https://docs.djangoproject.com/en/dev/topics/email/#testing-e-mail-sending
# http://blog.danawoodman.com/blog/2011/09/11/testing-email-sending-locally-in-django/
# In terminal:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
# EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD
# EMAIL_USE_TLS

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/static/files/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://127.0.0.1:8000/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mysecrethere-obviously-pick-something-different-and-long-and-complicated-and-do-not-share'