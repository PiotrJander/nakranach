from django.contrib.auth import login, logout
from django.db.transaction import atomic

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


from open_facebook import OpenFacebook

from app.users.models import Profile

class FacebookAuthenticate(APIView):
    model = Profile

    def post(self, request, format=None):
        email = request.data['email']
        access_token = request.data['access_token']

        graph = OpenFacebook(access_token)
        
        if graph.is_authenticated():
            self._authenticate_user(request, email, graph)
            return Response({'result': 'success'})
        else:
            return Response({'error': 'User is not authenticated on Facebook'}, status=401)

    @atomic
    def _authenticate_user(self, request, email, graph):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except:
            user = User.objects.create(email=email)
            profile = Profile.objects.create(avatar_url=graph.my_image_url(), user=user)

        # http://stackoverflow.com/a/2787747/2021915
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

class Logout(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    model = Profile

    def get(self, request, format=None):
        logout(request)
        return Response({'result': 'success'})