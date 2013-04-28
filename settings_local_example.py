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

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/static/files/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://127.0.0.1:8000/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mysecrethere-obviously-pick-something-different-and-long-and-complicated-and-do-not-share'