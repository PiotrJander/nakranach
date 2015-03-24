from rest_framework.permissions import IsAuthenticated

from django.contrib.sessions.models import Session
from django.utils import timezone

import datetime

SESSION_KEY = 'sessionid'

class IsAuthenticatedOrAnonymous(IsAuthenticated):
    def has_permission(self, request, view):
        result = super(IsAuthenticatedOrAnonymous, self).has_permission(request, view)

        request.is_api_call = True
        if not result:
            try:
                session_key = request.COOKIES[SESSION_KEY]
                session = Session.objects.get(session_key=session_key)

                now = timezone.now()

                result = now < session.expire_date

                request.is_api_call = False
            except:
                pass

        return result

class IsAPIUser(IsAuthenticated):
    def has_permission(self, request, view):
        api_user = getattr(request, 'api_user', None)
        return api_user is not None and api_user.is_authenticated()