# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orderable.models import Orderable

from geopy.geocoders import Nominatim

from app.beers.models import Beer

from uuslug import uuslug

class Pub(models.Model):
    name = models.CharField(verbose_name=_(u'Nazwa'), max_length=200)

    slug = models.CharField(max_length=200, editable=False)
    
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=250, blank=True)
    
    latitude = models.DecimalField(max_digits=6, decimal_places=3, editable=False, null=True, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3, editable=False, null=True, blank=True)

    avatar = models.ImageField(upload_to='pubs', blank=True, null=True)
    
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

class Volume(models.Model):
    pub = models.ForeignKey(Pub, related_name='available_volumes')
    value = models.PositiveIntegerField(verbose_name=_(u'Objętość'), help_text=_(u'W ml'))

    def __unicode__(self):
        return u'%s ml' % self.value
    
class Tap(models.Model):
    TAP_TYPES = (
        ('pump', _(u'Pompa')),
        ('tap', _(u'Kran')),
    )

    sort_order = models.PositiveIntegerField(default=0)

    pub = models.ForeignKey(Pub, related_name='taps', blank=False, null=False)
    beer = models.ForeignKey(Beer, related_name='taps', blank=True, null=True)

    type = models.CharField(_(u'Rodzaj kranu'), max_length=32, choices=TAP_TYPES, default='tap')

    class Meta:
        ordering = ('sort_order',)
        unique_together = ('pub', 'sort_order')

    def __unicode__(self):
        return '%s tap #%s' % (self.pub, self.sort_order)


class Price(models.Model):
    tap = models.ForeignKey(Tap, related_name='prices')
    volume = models.ForeignKey(Volume, related_name='prices')

    # the max_digits value is set to cover border case
    # when Papiernik orders a beer which is brewed by 
    # 25 year old virgins in Tibetan Plateu from yak's
    # milk which was fed only with lotus flowers
    value = models.DecimalField(max_digits=10, decimal_places=2)

class WaitingBeer(models.Model):
    pub = models.ForeignKey(Pub, blank=False, null=False)
    beer = models.ForeignKey(Beer, blank=False, null=False)
