# -*- coding: utf-8 -*-

USER_KEY = 'api_user'

def login_user(request, user):
    request.session[USER_KEY] = user.email

def logout_user(request):
    request.session[USER_KEY] = None

class APIUserMiddleware(object):
    def process_request(self, request):
        from django.contrib.auth import get_user_model

        try:
            User = get_user_model()

            email = request.session.get(USER_KEY, None)

            if email is not None:
                user = User.objects.get(email=email)
                request.api_user = user

        except User.DoesNotExist:
            request.session[USER_KEY] = None