# Django settings for acubor project.

import os
import django


# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Acubor Inc.', 'app@acubor.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

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
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = SITE_ROOT + '/static_files/'

ADMIN_MEDIA_PREFIX = '/admin_media/'

# Additional locations of static files
# STATICFILES_DIRS = (
#     SITE_ROOT + '/static/',
# )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2h7ffi6+vhk!dfi1#kn+(zm%gl2!8m)zv9g*%0+!3q+oujqb!y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    'users.middleware.RoleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'acubor.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'acubor.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, '..', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'south',
    'core',
    'users',
    # 'registration',
    'inventory',
    'tax',
    'voucher',
    'ledger',
    'dayjournal',
    'payroll',
    'bank',
    'report',
    # 'blog',
    'redactor',
    'mptt',
    'debug_toolbar',
    'pagination',
    'django_sorting',
    # 'gunicorn',
    # 'sorter',
    'rest_framework',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
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

try:
    from settings_secret import *
except ImportError:
    pass

AUTH_USER_MODEL = 'users.User'

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/user/login/'

AUTHENTICATION_BACKENDS = (
    'users.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend'
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'redactor_uploads/'