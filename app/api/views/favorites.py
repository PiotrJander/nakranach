# -*- coding: utf-8 -*-

from django.core.exceptions import  ObjectDoesNotExist
from rest_framework.generics import GenericAPIView, ListAPIView

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from django.http import Http404

from oauth2_provider.ext.rest_framework import OAuth2Authentication

from app.pubs.models import Pub
from app.users.models import Profile
from app.taps.models import TapChange

from app.api.serializers import PubSerializer, TapChangeSerializer
from app.api.pagination import PubListPagination, TapChangePagination
from app.api.permissions import IsAPIUser

class FavoritesListView(ListAPIView):
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAPIUser,)

    serializer_class = PubSerializer
    pagination_class = PubListPagination

    def get_queryset(self):
        try:
            return self.request.api_user.profile.favorite_pubs.all()
        except ObjectDoesNotExist:
            return Pub.objects.none()

class ToggleFavoriteView(GenericAPIView):
    queryset = Pub.objects.all()

    serializer_class = PubSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAPIUser,)

    def post(self, request, slug, format=None):
        try:
            pub =  self.queryset.get(slug=slug)
            profile = request.api_user.profile

            if profile.favorite_pubs.filter(pk=pub.pk).exists():
                profile.favorite_pubs.remove(pub)
            else:
                profile.favorite_pubs.add(pub)

            serializer = self.serializer_class(pub, many=False, context={'request': request})

            return Response(serializer.data)
        except (Pub.DoesNotExist, ObjectDoesNotExist):
            raise Http404

class FavoriteTapChanges(ListAPIView):
    queryset = TapChange.objects.all()

    serializer_class = TapChangeSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAPIUser,)

    pagination_class = TapChangePagination

    def get_queryset(self):
        try:
            pubs = self.request.api_user.profile.favorite_pubs.all()
            return self.queryset.filter(tap__pub__in=pubs)
        except ObjectDoesNotExist:
            return self.queryset.none()
