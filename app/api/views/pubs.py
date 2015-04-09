from django.db.transaction import atomic
from django.http import Http404

from rest_framework import mixins, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from oauth2_provider.ext.rest_framework import OAuth2Authentication

from app.pubs import models as pubs_models
from app.taps import models as taps_models
from app.beers import models as beer_models

from app.api.serializers import PubSerializer, TapSerializer, BeerSerializer, TapChangeSerializer, WaitingBeerSerializer
from app.api.permissions import IsPubManager

from .helpers import tap_changes_response
from .mixins import AuthMixin
from app.api.pagination import TapChangePagination, PubListPagination, TapListPagination, BeerPagination, WaitingBeerPagination

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

    pagination_class = WaitingBeerPagination
    serializer_class = WaitingBeerSerializer

    def get(self, request, slug, format=None):
        pub = self.get_pub(slug)

        self.check_object_permissions(request, pub)

        qs = pubs_models.WaitingBeer.objects.filter(pub=pub)
        return self.get_response(qs)

class ChangeBeerView(PubDetailView):
    authentication_classes = (OAuth2Authentication, SessionAuthentication,)
    permission_classes = (IsPubManager,)

    @atomic
    def post(self, request, slug, format=None):
        pub = self.get_pub(slug)
        self.check_object_permissions(request, pub)

        tap_pk = None
        beer_pk = None

        tap = None
        beer = None
        waiting_beer = None

        try:
            tap_pk = request.data['tap']
        except KeyError, e:
            return Response({'error': 'Field "%s" is required' % e.args[0]}, status=400)

        beer_pk = request.data.get('beer', None)

        try:
            tap = pub.taps.get(pk=tap_pk)
        except pubs_models.Tap.DoesNotExist:
            return Response({'error': 'Tap is undefined'}, status=404)

        try:
            if beer_pk is not None:
                beer = beer_models.Beer.objects.get(pk=beer_pk)
                waiting_beer = pubs_models.WaitingBeer.objects.get(beer=beer, pub=tap.pub)
            else:
                beer = None
        except beer_models.Beer.DoesNotExist:
            return Response({'error': 'Beer is undefined'}, status=404)
        except pubs_models.WaitingBeer.DoesNotExist:
            return Response({'error': 'Beer is not available in selected pub'}, status=404)

        previous_beer = tap.beer

        tap.beer = beer
        tap.save()

        if beer is not None:
            tap.prices.all().delete()

            for price in waiting_beer.prices.all():
                price.copy_to_tap(tap)

        tap_change = taps_models.TapChange.objects.create(tap=tap,
                                                    previous_beer=previous_beer,
                                                    new_beer=beer,
                                                    user=request.api_user.profile)

        serializer = TapChangeSerializer(tap_change, many=False, context={'request': request})
        return Response(serializer.data)