from rest_framework.permissions import IsAuthenticated

from django.contrib.sessions.models import Session
from django.utils import timezone

import datetime

SESSION_KEY = 'sessionid'

class IsAuthenticatedOrAnonymous(IsAuthenticated):
    def has_permission(self, request, view):
        result = super(IsAuthenticatedOrAnonymous, self).has_permission(request, view)
        if not result:
            try:
                session_key = request.COOKIES[SESSION_KEY]
                session = Session.objects.get(session_key=session_key)

                now = timezone.now()

                result = now < session.expire_date
            except:
                pass

        return result