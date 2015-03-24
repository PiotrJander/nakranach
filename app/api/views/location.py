# -*- coding: utf-8 -*-

from haversine import haversine
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from app.pubs.models import Pub

from app.api.serializers import PubSerializer

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
    queryset = Pub.objects.all()
    serializer_class = PubSerializer

    def list(self, request, *args, **kwargs):
        nearest_pubs = self.get_nearest_pubs()
        serializer = self.serializer_class(nearest_pubs, many=True, context={'request': request})
        return Response(serializer.data)