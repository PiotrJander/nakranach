from django.contrib.auth import login, logout
from django.db.transaction import atomic

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.ext.rest_framework import OAuth2Authentication

from open_facebook import OpenFacebook

from app.users.models import Profile
from app.api.serializers import ProfileSerializer


import md5

# TODO: add request checking

USER_KEY = 'user'

def login_user(request, user):
    request.session[USER_KEY] = user.email

def logout_user(request):
    request.session[USER_KEY] = None

def get_gravatar_url(email):
    trimmed_email = email.strip().lower()
    hash = md5.new(trimmed_email).hexdigest()
    return 'http://www.gravatar.com/avatar/%s' % hash

def profile_response(profile):
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

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
            print 'logging ', user
            if user.password and user.check_password(password):
                login_user(request, user)
                return profile_response(user.profile)

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

            name = request.data.get('name', None)
            surname = request.data.get('surname', None)
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

        profile = Profile.objects.create(avatar_url=get_gravatar_url(email), user=user, name=name, surname=surname)
        login_user(request, user)
        return profile_response(profile)

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
            profile = self._authenticate_user(request, email, graph)
            return profile_response(profile)
        else:
            return Response({'error': 'User is not authenticated on Facebook'}, status=401)

    @atomic
    def _authenticate_user(self, request, email, graph):
        profile = None

        try:
            user = self.user_class.objects.get(email=email)
            profile = user.profile
        except self.user_class.DoesNotExist:
            user = self.user_class.objects.create(email=email)

            me = graph.me()
            picture = graph.get('me/picture', redirect=False)
            avatar_url = None

            name = me.get('first_name', None)
            surname = me.get('last_name', None)

            if picture['data']['is_silhouette']:
                avatar_url = get_gravatar_url(email)
            else:
                avatar_url = picture['data']['url']

            profile = Profile.objects.create(avatar_url=avatar_url, user=user, name=name, surname=surname)

        login_user(request, user)
        return profile

class Logout(BaseAuthView):
    authentication_classes = (OAuth2Authentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    model = Profile

    def get(self, request, format=None):
        logout_user(request)
        return Response({'result': 'success'})