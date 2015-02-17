# -*- coding: utf-8 -*-

from django.db import models

from orderable.models import Orderable

from geopy.geocoders import Nominatim

from app.beers.models import Beer

from uuslug import uuslug

class Pub(models.Model):
    name = models.CharField(verbose_name='Nazwa', max_length=200)

    slug = models.CharField(max_length=200, editable=False)
    
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=250, blank=True)
    
    latitude = models.DecimalField(max_digits=6, decimal_places=3, editable=False, null=True, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3, editable=False, null=True, blank=True)    
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        
        geolocator = Nominatim()
        location = geolocator.geocode("%s, %s" % (self.address, self.city))
        
        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude
        
        super(Pub, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/%s' % self.slug
    
class Tap(Orderable):
    TAP_TYPES = (
        ('pump', 'Pompa'),
        ('tap', 'Kran'),
    )

    pub = models.ForeignKey(Pub, related_name='taps', blank=False, null=False)
    beer = models.ForeignKey(Beer, related_name='taps', blank=True, null=True)

    type = models.CharField(u'Rodzaj kranu', max_length=32, choices=TAP_TYPES, default='tap')

class WaitingBeer(models.Model):
    pub = models.ForeignKey(Pub, blank=False, null=False)
    beer = models.ForeignKey(Beer, blank=False, null=False)
