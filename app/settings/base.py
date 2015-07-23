# -*- coding: utf-8 -*-

import os

_ = gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__)) + '/../'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '50qwz*@_w**hcydw&o&tlbw%041gs_ftw!qo%dog%)_0py#w9&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'app.api.middleware.APIUserMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH) + '/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'haystack',
    'oauth2_provider',
    'rest_framework',
    'custom_user',
    'crispy_forms',
    'app.beers',
    'app.pubs',
    'app.taps',
    'app.api',
    'app.users',
    'app.fb',
    'registration',

    # possibly
    'bootstrapform',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',

    # custom
    'app.main.context_processors.sidebar_menu',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTH_USER_MODEL = 'custom_user.EmailUser'

LANGUAGES = [
    ('pl', 'Polski'),
]

SITE_ID = 1

SESSION_SAVE_EVERY_REQUEST = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_CLASS_CONVERTERS = {'textinput': "textinput text-input"}

FIXTURE_DIRS = [
    os.path.join(PROJECT_PATH, 'fixtures')
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_PATH, '..', 'indexes', 'whoosh_index'),
    },
}

# login
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

# registration
REGISTRATION_AUTO_LOGIN = True
INCLUDE_REGISTER_URL = False
INCLUDE_AUTH_URLS = True
# REGISTRATION_FORM = 'app.users.forms.CustomUserRegistrationForm'

from .api import *
from .fb import *
