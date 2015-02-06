# -*- coding: utf-8 -*-

from rest_framework import serializers

from app.pubs import models as pubs_models
from app.taps import models as taps_models

class PubSerializer(serializers.HyperlinkedModelSerializer):
    taps = serializers.HyperlinkedIdentityField(view_name='pub-taps')

    class Meta:
        model = pubs_models.Pub
        fields = ('name', 'slug', 'city', 'address', 'longitude', 'latitude', 'taps')

class TapSerializer(serializers.ModelSerializer):
    class Meta:
        model = pubs_models.Tap
        fields = ('id', 'sort_order', 'type')
