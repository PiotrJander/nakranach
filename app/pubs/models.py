# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile

from orderable.models import Orderable

from geopy.geocoders import Nominatim

from app.beers.models import Beer

from PIL import Image

import StringIO
import os

from uuslug import uuslug

AVATAR_SIZE = (256, 256)

class Pub(models.Model):
    name = models.CharField(verbose_name=_(u'Nazwa'), max_length=200)

    slug = models.CharField(max_length=200, editable=False)
    
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=250, blank=True)
    
    latitude = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    avatar = models.ImageField(upload_to='pubs', blank=True, null=True, help_text=_(u'Preferred size is 256x256. If uploaded image has different size, it will be resized automatically'))
    avatar_timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    opens = models.TimeField()
    closes = models.TimeField()

    waiting_beers = models.ManyToManyField(Beer, through='WaitingBeer', through_fields=('pub', 'beer'), related_name='waiting_in_pubs')
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        
        # this allows specification of raw coordinates in admin
        if self.latitude is None or self.longitude is None:
            geolocator = Nominatim()
            location = geolocator.geocode("%s, %s" % (self.address, self.city))
            
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
        
        super(Pub, self).save(*args, **kwargs)

        if self.avatar is not None:
            avatar_image = Image.open(self.avatar)

            current_size = avatar_image.size

            filename, extension = os.path.splitext(os.path.basename(self.avatar.name))

            if current_size[0] != AVATAR_SIZE[0] or current_size[1] != AVATAR_SIZE[1] or extension != '.png':
                avatar_image = avatar_image.resize(AVATAR_SIZE, Image.ANTIALIAS)

                output = StringIO.StringIO()

                avatar_image.save(output, 'png')

                filename = '%s.png' % filename
                image_file = InMemoryUploadedFile(output, None, filename, 'image/png', output.len, None)
                
                self.avatar.save(filename, image_file)
                output.close()

    def get_absolute_url(self):
        return '/%s' % self.slug

    @property
    def is_open(self):
        now = timezone.now()
        now_time = now.time()

        is_open = (now_time >= self.opens and now_time <= self.closes)

        return is_open

    def get_taps(self):
        return Tap.objects.filter(pub=self)

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(pk=id)


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

    @property
    def tap_number(self):
        return self.sort_order + 1

    class Meta:
        ordering = ('sort_order',)
        unique_together = ('pub', 'sort_order')

    def __unicode__(self):
        return u'%s tap #%s' % (self.pub, self.sort_order)


class WaitingBeer(models.Model):
    pub = models.ForeignKey(Pub, blank=False, null=False)
    beer = models.ForeignKey(Beer, blank=False, null=False)

    def __unicode__(self):
        return u'%s - %s' % (self.pub, self.beer)

class Price(models.Model):
    tap = models.ForeignKey(Tap, related_name='prices', null=True, blank=True)
    beer = models.ForeignKey(WaitingBeer, related_name='prices', null=True, blank=True)
    
    volume = models.ForeignKey(Volume, related_name='prices')

    # the max_digits value is set to cover border case
    # when Papiernik orders a beer which is brewed by 
    # 25 year old virgins in Tibetan Plateu from yak's
    # milk which was fed only with lotus flowers
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def copy_to_tap(self, tap):
        if self.beer is None:
            raise AttributeError(_(u'Beer is not set - cannot copy to tap'))

        copy = Price(tap=tap, beer=None, volume=self.volume, value = self.value)
        copy.save()

        return copy
