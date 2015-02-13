# -*- coding: utf-8 -*-

from rest_framework import serializers

from app.pubs import models as pubs_models
from app.taps import models as taps_models
from app.beers import models as beer_models

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
    taps = serializers.HyperlinkedIdentityField(view_name='pub-taps')
    tap_changes = serializers.HyperlinkedIdentityField(view_name='pub-tap-changes')

    class Meta:
        model = pubs_models.Pub
        fields = ('name', 'slug', 'city', 'address', 'longitude', 'latitude', 'taps', 'tap_changes')

class TapSerializer(serializers.HyperlinkedModelSerializer):
    pub = serializers.HyperlinkedRelatedField(view_name='pub-view', read_only=True)
    beer = BeerSerializer(read_only=True)

    class Meta:
        model = pubs_models.Tap
        fields = ('sort_order', 'type', 'pub', 'beer')

class TapChangeSerializer(serializers.ModelSerializer):
    tap = TapSerializer(read_only=True)
    previous_beer = BeerSerializer(read_only=True)
    new_beer = BeerSerializer(read_only=True)

    class Meta:
        model = taps_models.TapChange
        fields = ('timestamp', 'previous_beer', 'new_beer', 'tap')
