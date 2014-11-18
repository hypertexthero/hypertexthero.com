# Django settings for hth project.

import os
DIRNAME = os.path.dirname(__file__)

TIME_FORMAT = 'H-i-s'
DATE_FORMAT = 'Y-F-j'# This is used by the SelectDateWidget in django.forms.extras.widgets http://stackoverflow.com/a/6137099/412329
DATETIME_FORMAT = 'Y-F-j H-i-s'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True # https://docs.djangoproject.com/en/dev/topics/cache/#the-per-site-cache

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

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

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
    'honeypot.middleware.HoneypotMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

HONEYPOT_FIELD_NAME = 'streetaddress'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    # need to add the following so user variables such as username are available in templates - https://docs.djangoproject.com/en/dev/ref/templates/api/#django-contrib-auth-context-processors-auth
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django_browserid.context_processors.browserid',
)

ROOT_URLCONF = 'hth.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hth.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
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

    # =mozilla =persona authentication
    'django_browserid',

    'typogrify',
    'markdown',

    # python manage.py staticsitegen
    # 'django_medusa',
    'staticgenerator',

    'taggit',
    'taggit_autosuggest',
    'taggit_templatetags2', # https://github.com/fizista/django-taggit-templatetags2
    
    # application server
    'gunicorn',
    
    # stop spam
    'honeypot',
    
    # see what's running: ps aux | grep gunicorn
    # graceful stop: kill -HUP ####
    # start: gunicorn --daemon wsgi:application -b 127.0.0.1:23035
    #    or: python manage.py run_gunicorn --daemon -b 127.0.0.1:23035 -w 2 --max-requests 500
    # stop: pkill gunicorn

    'contact_form',
    'hth.templatetags',
    'hth',
)

# =mozilla =persona
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.BrowserIDBackend',
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

# database, secret key, email settings, etc are in settings_local.py
try:
    from settings_local import *
except ImportError:
    pass