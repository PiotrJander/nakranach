from django.http import Http404

from rest_framework import mixins, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from app.api.permissions import IsAuthenticatedOrAnonymous
from app.pubs import models as pubs_models
from app.taps import models as taps_models

from app.api.serializers import PubSerializer, TapSerializer

from .helpers import tap_changes_response

# view classes
class AuthMixin(object):
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAuthenticatedOrAnonymous,)

class PubList(AuthMixin, mixins.ListModelMixin,
                generics.GenericAPIView):
    queryset = pubs_models.Pub.objects.all()
    serializer_class = PubSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class PubDetailView(AuthMixin, APIView):
    # http://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    queryset = pubs_models.Pub.objects.all()

    def get_pub(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except pubs_models.Pub.DoesNotExist:
            raise Http404

class PubView(PubDetailView):
    def get(self, request, pk, format=None):
        pub = self.get_pub(pk)
        serializer = PubSerializer(pub, many=False, context={'request': request})
        return Response(serializer.data)

class TapList(PubDetailView):
    def get(self, request, pk, format=None):
        pub = self.get_pub(pk)
        serializer = TapSerializer(pub.taps, many=True, context={'request': request})
        return Response(serializer.data)

class TapChangeList(PubDetailView):
    def get(self, request, pk, format=None):
        pub = self.get_pub(pk)
        tap_ids = [tap.pk for tap in pub.taps.all()]
        return tap_changes_response(
            taps_models.TapChange.objects.filter(tap_id__in=tap_ids),
            request,
            5
        )