# -*- coding: utf-8 -*-

from rest_framework import serializers

from app.pubs import models as pubs_models
from app.taps import models as taps_models
from app.beers import models as beer_models

class RequestAwareHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        is_api_call = getattr(request, 'is_api_call', False)

        if is_api_call:
            view_name = 'api-%s' % view_name

        return super(RequestAwareHyperlinkedRelatedField, self).get_url(obj, view_name, request, format)

class BrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = beer_models.Brewery
        fields = ('name', 'country')

class BeerSerializer(serializers.ModelSerializer):
    brewery = BrewerySerializer(read_only=True)
    style = serializers.StringRelatedField()

    class Meta:
        model = beer_models.Beer
        fields = ('name', 'ibu', 'abv', 'brewery', 'style')

class PubSerializer(serializers.HyperlinkedModelSerializer):
    taps = serializers.HyperlinkedIdentityField(view_name='api-pub-taps', lookup_field='slug')
    tap_changes = serializers.HyperlinkedIdentityField(view_name='api-pub-tap-changes', lookup_field='slug')
    
    class Meta:
        model = pubs_models.Pub
        fields = ('name', 'slug', 'city', 'address', 'longitude', 'latitude', 'taps', 'tap_changes', 'avatar')

class TapSerializer(serializers.HyperlinkedModelSerializer):
    pub = RequestAwareHyperlinkedRelatedField(view_name='pub-view', read_only=True, lookup_field='slug')
    pub_name = serializers.StringRelatedField(source='pub')
    beer = BeerSerializer(read_only=True)
    pub_slug = serializers.CharField(source='pub.slug')

    class Meta:
        model = pubs_models.Tap
        fields = ('sort_order', 'type', 'pub', 'pub_name', 'beer', 'pub_slug')

class TapChangeSerializer(serializers.ModelSerializer):
    tap = TapSerializer(read_only=True)
    previous_beer = BeerSerializer(read_only=True)
    new_beer = BeerSerializer(read_only=True)
    
    class Meta:
        model = taps_models.TapChange
        fields = ('timestamp', 'previous_beer', 'new_beer', 'tap')
