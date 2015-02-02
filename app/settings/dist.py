from .base import *

from .db import DATABASES

# Debugging
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
]

# Admins
ADMINS = (
    ('Mateusz Papiernik', 'biuro@makimo.pl'),
)

# Media and statics
MEDIA_ROOT = os.path.join(PROJECT_PATH) + '/../uploads/'
MEDIA_URL = "/uploads/"

# Production static dir
STATIC_ROOT = os.path.join(PROJECT_PATH) + '/../static/dist/'
STATIC_URL = "/static/"

# Email
SERVER_EMAIL = 'biuro@makimo.pl'
DEFAULT_FROM_EMAIL = 'biuro@makimo.pl'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

