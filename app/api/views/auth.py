from django.contrib.auth import login, logout
from django.db.transaction import atomic

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.ext.rest_framework import OAuth2Authentication

from open_facebook import OpenFacebook

from app.users.models import Profile

import md5

# TODO: add request checking

def login_user(request, user):
    # http://stackoverflow.com/a/2787747/2021915
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

def get_gravatar_url(email):
    trimmed_email = email.strip().lower()
    hash = md5.new(trimmed_email).hexdigest()
    return 'http://www.gravatar.com/avatar/%s' % hash

class BaseAuthView(APIView):
    def __init__(self, *args, **kwargs):
        super(BaseAuthView, self).__init__(*args, **kwargs)

        from django.contrib.auth import get_user_model
        self.user_class = get_user_model()

class Login(BaseAuthView):
    authentication_classes = (OAuth2Authentication,)
    model = Profile

    def post(self, request, format=None):
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError, e:
            return Response({'error': 'Field "%s" is required' % e.args[0]}, status=400)

        try:
            user = self.user_class.objects.get(email=email)
            if user.password and user.check_password(password):
                login_user(request, user)
                return Response({'result': 'success'})
        except self.user_class.DoesNotExist:
            pass

        return Response({'error': 'Invalid credentials'}, status=401)

class Register(BaseAuthView):
    authentication_classes = (OAuth2Authentication,)
    model = Profile

    def post(self, request, format=None):
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError, e:
            return Response({'error': 'Field "%s" is required' % e.args[0]}, status=400)

        try:
            user = self.user_class.objects.get(email=email)
            return Response({'error': 'User already exists'}, status=401)
        except self.user_class.DoesNotExist:
            pass

        user = self.user_class(email=email, is_superuser=False, is_active=True, is_staff=False)
        user.set_password(password)
        user.save()

        Profile.objects.create(avatar_url=get_gravatar_url(email), user=user)

        login_user(request, user)

        return Response({'result': 'success'})

class FacebookAuthenticate(BaseAuthView):
    authentication_classes = (OAuth2Authentication,)
    model = Profile

    def post(self, request, format=None):
        try:
            email = request.data['email']
            access_token = request.data['access_token']
        except KeyError, e:
            return Response({'error': 'Field "%s" is required' % e.args[0]}, status=400)

        graph = OpenFacebook(access_token)
        
        if graph.is_authenticated():
            self._authenticate_user(request, email, graph)
            return Response({'result': 'success'})
        else:
            return Response({'error': 'User is not authenticated on Facebook'}, status=401)

    @atomic
    def _authenticate_user(self, request, email, graph):
        try:
            user = self.user_class.objects.get(email=email)
        except self.user_class.DoesNotExist:
            user = self.user_class.objects.create(email=email)

            picture = graph.get('me/picture', redirect=False)
            avatar_url = None

            if picture['data']['is_silhouette']:
                avatar_url = get_gravatar_url(email)
            else:
                avatar_url = picture['data']['url']

            profile = Profile.objects.create(avatar_url=avatar_url, user=user)

        login_user(request, user)

class Logout(BaseAuthView):
    authentication_classes = (OAuth2Authentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    model = Profile

    def get(self, request, format=None):
        logout(request)
        return Response({'result': 'success'})