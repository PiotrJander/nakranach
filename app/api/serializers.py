# -*- coding: utf-8 -*-

from rest_framework import serializers

from app.pubs import models as pubs_models
from app.taps import models as taps_models
from app.beers import models as beer_models
from app.users import models as user_models

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

class PriceSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='value')
    volume = serializers.IntegerField(source='volume.value')

    class Meta:
        model = pubs_models.Price
        fields = ('volume', 'price')

class BeerSerializer(serializers.ModelSerializer):
    brewery = BrewerySerializer(read_only=True)
    style = serializers.StringRelatedField()

    class Meta:
        model = beer_models.Beer
        fields = ('id', 'name', 'ibu', 'abv', 'brewery', 'style')

class WaitingBeerSerializer(BeerSerializer):
    id = serializers.IntegerField(source='beer.id')
    name = serializers.CharField(source='beer.name')
    ibu = serializers.IntegerField(source='beer.ibu')
    abv = serializers.DecimalField(source='beer.abv', max_digits=3, decimal_places=1)
    brewery = BrewerySerializer(source='beer.brewery', read_only=True)
    style = serializers.StringRelatedField(source='beer.style')
    prices = PriceSerializer(many=True)

    class Meta:
        model = pubs_models.WaitingBeer
        fields = ('id', 'name', 'ibu', 'abv', 'brewery', 'style', 'prices')        

class PubSerializer(serializers.HyperlinkedModelSerializer):
    taps = serializers.HyperlinkedIdentityField(view_name='api-pub-taps', lookup_field='slug')
    tap_changes = serializers.HyperlinkedIdentityField(view_name='api-pub-tap-changes', lookup_field='slug')
    is_open = serializers.BooleanField()
    
    class Meta:
        model = pubs_models.Pub
        fields = ('name', 'slug', 'city', 'address', 'longitude', 'latitude', 'taps', 'tap_changes', 'avatar', 'avatar_timestamp', 'is_open')

    @property
    def favorites(self):
        if hasattr(self, '_favorites') and self._favorites is not None:
            return self._favorites

        if 'request' in self.context:
            request = self.context['request']

            if hasattr(request, 'api_user'):
                user = request.api_user
                self._favorites = [pub.pk for pub in user.profile.favorite_pubs.all()]
                return self._favorites

        return []

    def to_representation(self, obj):
        result = super(PubSerializer, self).to_representation(obj)

        result['is_favorite'] = obj.pk in self.favorites

        return result

class ManagedPubSerializer(PubSerializer):
    waiting_beers = serializers.HyperlinkedIdentityField(view_name='api-pub-waiting-beers', lookup_field='slug')
    change_beer = serializers.HyperlinkedIdentityField(view_name='api-pub-change-beer', lookup_field='slug')

    class Meta(PubSerializer.Meta):
        fields = ('name', 'slug', 'city', 'address', 'longitude', 'latitude', 'taps', 'tap_changes', 'avatar', 'is_open', 'waiting_beers', 'change_beer')

class TapSerializer(serializers.HyperlinkedModelSerializer):
    pub = PubSerializer(read_only=True)
    pub_name = serializers.StringRelatedField(source='pub')
    beer = BeerSerializer(read_only=True)
    pub_slug = serializers.CharField(source='pub.slug')
    prices = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = pubs_models.Tap
        fields = ('id', 'sort_order', 'type', 'pub', 'pub_name', 'beer', 'pub_slug', 'prices')

    def to_representation(self, obj):
        result = super(TapSerializer, self).to_representation(obj)

        result['sort_order'] = obj.tap_number

        return result

class TapChangeSerializer(serializers.ModelSerializer):
    tap = TapSerializer(read_only=True)
    pub = PubSerializer(read_only=True)
    previous_beer = BeerSerializer(read_only=True)
    new_beer = BeerSerializer(read_only=True)
    
    class Meta:
        model = taps_models.TapChange
        fields = ('timestamp', 'pub', 'previous_beer', 'new_beer', 'tap')

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    can_manage_pubs = serializers.BooleanField()
    managed_pubs = ManagedPubSerializer(read_only=True, many=True, source='pubs')

    class Meta:
        model = user_models.Profile
        fields = ('avatar_url', 'email', 'name', 'surname', 'can_manage_pubs', 'managed_pubs')
