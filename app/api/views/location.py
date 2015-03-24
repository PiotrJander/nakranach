# -*- coding: utf-8 -*-

from haversine import haversine
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from app.pubs.models import Pub
from app.taps.models import TapChange

from app.api.serializers import PubSerializer, TapChangeSerializer

MINIMAL_DISTANCE = 0.5
MAXIMAL_DISTANCE = 10.0
STEP = 0.5

class PubLocationMixin(object):
    def get(self, request, *args, **kwargs):
        self._location = (float(request.GET.get('latitude', 0.0)), float(request.GET.get('longitude', 0.0)))

        return super(PubLocationMixin, self).get(request, *args, **kwargs)

    def get_nearest_pubs(self):
        queryset = Pub.objects.all()

        pubs = []
        buckets = [[] for _ in range(int(MINIMAL_DISTANCE * 10), int(MAXIMAL_DISTANCE * 10), int(STEP * 10))]

        for pub in queryset:
            pub.distance = haversine(self._location, (pub.latitude, pub.longitude))

            if pub.distance >= MAXIMAL_DISTANCE:
                continue

            index = int(pub.distance / STEP)
            buckets[index].append(pub)

        for bucket in buckets:
            sorted(bucket, key=lambda pub: pub.distance)
            pubs.extend(bucket)

            if len(pubs) >= 3:
                break

        return pubs

class NearestPubsView(PubLocationMixin, ListAPIView):
    queryset = Pub.objects.none()
    serializer_class = PubSerializer

    def list(self, request, *args, **kwargs):
        nearest_pubs = self.get_nearest_pubs()
        serializer = self.serializer_class(nearest_pubs, many=True, context={'request': request})
        return Response(serializer.data)

class NearestActivitiesView(PubLocationMixin, ListAPIView):
    queryset = TapChange.objects.all()
    serializer_class = TapChangeSerializer

    def list(self, request, *args, **kwargs):
        nearest_pubs = self.get_nearest_pubs()

        activities = self.queryset.filter(tap__pub__in=nearest_pubs).order_by('-timestamp')[:15]
        serializer = self.serializer_class(activities, many=True, context={'request': request})
        return Response(serializer.data)