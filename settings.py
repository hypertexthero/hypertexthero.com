# Django settings for hth project.

import os
DIRNAME = os.path.dirname(__file__)

TIME_FORMAT = 'H-i-s'
DATE_FORMAT = 'Y-F-j'# This is used by the SelectDateWidget in django.forms.extras.widgets http://stackoverflow.com/a/6137099/412329
DATETIME_FORMAT = 'Y-F-j H-i-s'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True # https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Simon Griffee', 'simon@hypertexthero.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/Users/Simon/projects/hth-env/hth/hth.db', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(DIRNAME, 'static/files')

# ln -s ~/Projects/hth-env/lib/python2.7/site-packages/django/contrib/admin/static/admin/ ~/projects/hth-env/hth/hth/static/admin
ADMIN_MEDIA_PREFIX = '/static/admin/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/static/files/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(DIRNAME, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://127.0.0.1:8000/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/static/",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mysecrethere'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

APPEND_SLASH = True

MIDDLEWARE_CLASSES = (
    'staticgenerator.middleware.StaticGeneratorMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware', # enabling middleware for flatpages app
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware', # enabling redirects app
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    # need to add the following so user variables such as username are available in templates - https://docs.djangoproject.com/en/dev/ref/templates/api/#django-contrib-auth-context-processors-auth
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    # display django version in footer using template tag defined in context_processors.py - http://stackoverflow.com/questions/4256145/django-template-tag-to-display-django-version
    # 'phytosanitary.context_processors.django_version',
    # required to have login form on every page and for templatetags - http://stackoverflow.com/questions/2734055/putting-a-django-login-form-on-every-page
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'hth.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hth.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup', # enabling markup so we can have markdown. requires http://www.freewisdom.org/projects/python-markdown
    'django.contrib.flatpages', # enabling flatpages app
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'django.contrib.redirects', # enabling redirects app
    'django.contrib.sitemaps', # enabling sitemaps app

    'typogrify',
    'markdown',

    # python manage.py staticsitegen
    # 'django_medusa',
    'staticgenerator',

    'taggit',
    'taggit_autosuggest',

    'contact',
    'contact.templatetags',
    'hth.templatetags',
    
    'taggit',
    'hth',
)

# staticgenerator
WEB_ROOT = os.path.join(
    DIRNAME, '..', "_output"
)

# =todo: Static files should be generated automatically, and not after they have been visited once
STATIC_GENERATOR_URLS = (
    r'^/$',
    # r'^/()', # matches any page created?
    # (r'^$', 'direct_to_template', {'template': 'base.html'}),
    r'^/(logbook|linked|archive|work)',
    r'^/(?P<year>\d+)/(?P<month>\d{2})/$', 
    r'^/(?P<year>\d+)/$',
    # r'^/(archive)',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production backend?
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# or
# EMAIL_BACKEND = "mailer.backend.DbBackend"

# Testing Email Sending in local development environment
# https://docs.djangoproject.com/en/dev/topics/email/#testing-e-mail-sending
# http://blog.danawoodman.com/blog/2011/09/11/testing-email-sending-locally-in-django/
# In terminal:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
# EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD
# EMAIL_USE_TLS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# https://github.com/applegrew/django-select2/blob/master/testapp/testapp/settings.py
AUTO_RENDER_SELECT2_STATICS = False

#GENERATE_RANDOM_SELECT2_ID = True

##
# To test for multiple processes in developement system w/o WSGI, runserver at
# different ports. Use $('#select2_field_html_id').data('field_id') to get the id
# in one process. Now switch to another port and use
# $('#select2_field_html_id').data('field_id', "id from previous process") to set
# id from last process. Now try to use that field. Its ajax should still work and
# you should see a message like - "Id 7:2013-03-01 14:49:18.490212 not found in
# this process. Looking up in remote server.", in console if you have debug enabled.
##
#ENABLE_SELECT2_MULTI_PROCESS_SUPPORT = True
#SELECT2_MEMCACHE_HOST = '127.0.0.1' # Uncomment to use memcached too
#SELECT2_MEMCACHE_PORT = 11211       # Uncomment to use memcached too
#SELECT2_MEMCACHE_TTL = 9           # Default 900