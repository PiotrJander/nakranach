from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication

from app.api.permissions import IsAuthenticatedOrAnonymous

class AuthMixin(object):
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAuthenticatedOrAnonymous,)