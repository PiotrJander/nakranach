from .base import *

from .db import DATABASES

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = True

INSTALLED_APPS += ('debug_toolbar', 'template_timings_panel', 'sslserver', )

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings', 
]

# Admins
ADMINS = (
    ('Mateusz Papiernik', 'biuro@makimo.pl'),
)

MANAGERS = ADMINS

# Media and statics
MEDIA_ROOT = os.path.join(PROJECT_PATH) + '/../uploads/'
MEDIA_URL = "/uploads/"

# Production static dir - this is intended, development is served
# using STATICFILES_DIRS and staticfiles server, collectstatic is
# not used during development, and file copying is handled by Grunt
STATIC_ROOT = os.path.join(PROJECT_PATH) + '/../static/dist/'
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH) + '/../static/local/',
)

# Email
DEFAULT_FROM_EMAIL = 'biuro@makimo.pl'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DOMAIN = '127.0.0.1:8000'