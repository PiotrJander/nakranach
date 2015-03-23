from django.http import Http404

from rest_framework import mixins, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.pubs import models as pubs_models
from app.taps import models as taps_models

from app.api.serializers import PubSerializer, TapSerializer

from .helpers import tap_changes_response
from .mixins import AuthMixin
from app.api.pagination import TapChangePagination, PubListPagination, TapListPagination

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

class PubView(PubDetailView):
    def get(self, request, slug, format=None):
        pub = self.get_pub(slug)
        serializer = PubSerializer(pub, many=False, context={'request': request})
        return Response(serializer.data)

class TapList(PubDetailView):
    pagination_class = TapListPagination

    def get(self, request, slug, format=None):
        pub = self.get_pub(slug)

        qs = pub.taps
        pagination_enabled = self.paginator is not None

        if pagination_enabled:
            qs = self.paginator.paginate_queryset(qs, request, view=self)

        serializer = TapSerializer(pub.taps, many=True, context={'request': request})

        if pagination_enabled:
            return self.paginator.get_paginated_response(serializer.data)

        return Response(serializer.data)

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