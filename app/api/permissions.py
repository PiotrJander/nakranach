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

class IsPubManager(IsAPIUser):
    def has_permission(self, request, view):
        perm = super(IsPubManager, self).has_permission(request, view)

        if perm:
            perm = request.api_user.profile.can_manage_pubs

        return perm

    def has_object_permission(self, request, view, obj):
        if not request.api_user.profile.can_manage_pubs:
            return False

        return request.api_user.profile.pubs.filter(pk=obj.pk).exists()
