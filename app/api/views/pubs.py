from django.http import Http404

from rest_framework import mixins, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from oauth2_provider.ext.rest_framework import OAuth2Authentication

from app.pubs import models as pubs_models
from app.taps import models as taps_models

from app.api.serializers import PubSerializer, TapSerializer, BeerSerializer
from app.api.permissions import IsPubManager

from .helpers import tap_changes_response
from .mixins import AuthMixin
from app.api.pagination import TapChangePagination, PubListPagination, TapListPagination, BeerPagination

# view classes
class PubList(AuthMixin, mixins.ListModelMixin,
                generics.GenericAPIView):
    queryset = pubs_models.Pub.objects.all()
    serializer_class = PubSerializer
    lookup_field = 'slug'
    pagination_class = PubListPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class PubDetailView(AuthMixin, generics.GenericAPIView):
    # http://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    queryset = pubs_models.Pub.objects.all()

    def get_pub(self, slug):
        try:
            return self.queryset.get(slug=slug)
        except pubs_models.Pub.DoesNotExist:
            raise Http404

    def get_response(self, qs):
        pagination_enabled = self.paginator is not None

        if pagination_enabled:
            qs = self.paginator.paginate_queryset(qs, self.request, view=self)

        serializer = self.serializer_class(qs, many=True, context={'request': self.request})

        if pagination_enabled:
            return self.paginator.get_paginated_response(serializer.data)

        return Response(serializer.data)

class PubView(PubDetailView):
    def get(self, request, slug, format=None):
        pub = self.get_pub(slug)
        serializer = PubSerializer(pub, many=False, context={'request': request})
        return Response(serializer.data)

class TapList(PubDetailView):
    pagination_class = TapListPagination
    serializer_class = TapSerializer

    def get(self, request, slug, format=None):
        pub = self.get_pub(slug)
        qs = pub.taps
        return self.get_response(qs)

class TapChangeList(PubDetailView):
    pagination_class = TapChangePagination

    def get(self, request, slug, format=None):
        pub = self.get_pub(slug)
        tap_ids = [tap.pk for tap in pub.taps.all()]
        return tap_changes_response(
            taps_models.TapChange.objects.filter(tap_id__in=tap_ids),
            request,
            self
        )

class WaitingBeerList(PubDetailView):
    authentication_classes = (OAuth2Authentication, SessionAuthentication,)
    permission_classes = (IsPubManager,)

    pagination_class = BeerPagination
    serializer_class = BeerSerializer

    def get(self, request, slug, format=None):
        pub = self.get_pub(slug)

        self.check_object_permissions(request, pub)

        qs = pub.waiting_beers
        return self.get_response(qs)