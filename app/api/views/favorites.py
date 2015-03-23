# -*- coding: utf-8 -*-

from django.core.exceptions import  ObjectDoesNotExist
from rest_framework.generics import GenericAPIView, ListAPIView

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.ext.rest_framework import OAuth2Authentication

from app.pubs.models import Pub

from app.api.serializers import PubSerializer
from app.api.pagination import PubListPagination

class FavoritesListView(ListAPIView):
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = PubSerializer
    pagination_class = PubListPagination

    def get_queryset(self):
        try:
            return self.request.user.profile.favorite_pubs.all()
        except ObjectDoesNotExist:
            return Pub.objects.none()