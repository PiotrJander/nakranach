from django.http import Http404


from rest_framework import mixins, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.pubs import models as pubs_models

from .serializers import PubSerializer, TapSerializer

class PubList(mixins.ListModelMixin,
                generics.GenericAPIView):
    queryset = pubs_models.Pub.objects.all()
    serializer_class = PubSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class PubDetailView(APIView):
    # http://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    queryset = pubs_models.Pub.objects.all()

class TapList(PubDetailView):
    def get(self, request, pk, format=None):
        try:
            pub = self.queryset.get(pk=pk)
            serializer = TapSerializer(pub.taps, many=True)
            return Response(serializer.data)
        except pubs_models.Pub.DoesNotExist:
            raise Http404
