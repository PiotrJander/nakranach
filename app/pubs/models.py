# -*- coding: utf-8 -*-
import StringIO
import os
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from orderable.models import Orderable
from geopy.geocoders import Nominatim
from PIL import Image
from uuslug import uuslug
from app.beers.models import Beer, Brewery, Style

AVATAR_SIZE = (256, 256)


class Pub(models.Model):
    # required
    name = models.CharField(verbose_name=_(u'Nazwa'), max_length=200)
    city = models.CharField(max_length=200)

    # automatic
    slug = models.CharField(max_length=200, editable=False)
    avatar_timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    # optional
    waiting_beers = models.ManyToManyField(Beer, through='WaitingBeer', through_fields=('pub', 'beer'),
                                           related_name='waiting_in_pubs')

    address = models.CharField(max_length=250, blank=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    avatar = models.ImageField(upload_to='pubs', blank=True, help_text=_(
        u'Preferred size is 256x256. If uploaded image has different size, it will be resized automatically'))

    opens = models.TimeField(blank=True, null=True)
    closes = models.TimeField(blank=True, null=True)

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

        # FIXME with this code there is a ValueError on saving an instance when avatar is empty
        # if self.avatar is not None:
        #     avatar_image = Image.open(self.avatar)
        #
        #     current_size = avatar_image.size
        #
        #     filename, extension = os.path.splitext(os.path.basename(self.avatar.name))
        #
        #     if current_size[0] != AVATAR_SIZE[0] or current_size[1] != AVATAR_SIZE[1] or extension != '.png':
        #         avatar_image = avatar_image.resize(AVATAR_SIZE, Image.ANTIALIAS)
        #
        #         output = StringIO.StringIO()
        #
        #         avatar_image.save(output, 'png')
        #
        #         filename = '%s.png' % filename
        #         image_file = InMemoryUploadedFile(output, None, filename, 'image/png', output.len, None)
        #
        #         self.avatar.save(filename, image_file)
        #         output.close()

    def get_absolute_url(self):
        return '/%s' % self.slug

    @property
    def is_open(self):
        now = timezone.now()
        now_time = now.time()

        is_open = (now_time >= self.opens and now_time <= self.closes)

        return is_open

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(pk=id)

    def has_beer(self, beer_id):
        return self.waiting_beers.filter(id=beer_id).exists()

    def remove_beer(self, beer_id):
        self.waiting_beers.filter(id=beer_id).delete()


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
        return u'%s tap #%s' % (self.pub, self.sort_order)

    @property
    def tap_number(self):
        return self.sort_order + 1

    def description(self):
        return format_html('<span class="label label-danger new-circle span-left">{}</span> '
                           '<span class="label label-success new-circle span-left">{}</span>',
                           self.tap_number,
                           self.get_type_display())

    def empty(self, profile=None):
        self.beer = None
        self.save()

    def change_beer(self, new_beer, profile=None):
        self.beer = new_beer
        self.save()


class WaitingBeer(models.Model):
    pub = models.ForeignKey(Pub, blank=False, null=False)
    beer = models.ForeignKey(Beer, blank=False, null=False)

    _brewery = models.ForeignKey(Brewery, verbose_name=_('browar'), blank=True, null=True)
    _style = models.ForeignKey(Style, verbose_name=_('styl'), blank=True, null=True)
    _name = models.CharField(verbose_name=_('nazwa'), max_length=255, blank=True)
    _ibu = models.IntegerField(verbose_name=_('IBU'), null=True, blank=True)
    _abv = models.DecimalField(verbose_name=_('ABV'), null=True, blank=True, decimal_places=1, max_digits=3)

    def __unicode__(self):
        return u'%s - %s' % (self.pub, self.beer)

    def __init__(self, *args, **kwargs):
        super(WaitingBeer, self).__init__(*args, **kwargs)
        for field in ['brewery', 'style', 'name', 'ibu', 'abv']:
            field_private = '_%s' % field
            overriden = getattr(self, field_private)
            prop = property(lambda self:  overriden if overriden else getattr(self.beer, field))
            setattr(self, field, prop)


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

        copy = Price(tap=tap, beer=None, volume=self.volume, value=self.value)
        copy.save()

        return copy
