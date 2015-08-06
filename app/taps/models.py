# -*- coding: utf-8 -*-

from django.db import models

from django.utils.translation import ugettext_lazy as _

from app.beers.models import Beer
from app.pubs.models import Tap
from app.users.models import Profile

class TapChange(models.Model):
    class Meta:
        verbose_name = _('zmiana na kranie')
        verbose_name_plural = _('zmiany na kranach')

    tap = models.ForeignKey(Tap, verbose_name=_('tap'), editable=False)
    previous_beer = models.ForeignKey(Beer, verbose_name=_('poprzednie piwo'), related_name='+', editable=False,
                                      blank=True, null=True)
    new_beer = models.ForeignKey(Beer, verbose_name=_('nowe piwo'), related_name='+', editable=False, blank=True,
                                 null=True)
    timestamp = models.DateTimeField(verbose_name=_('czas'), auto_now_add=True, editable=False)
    user = models.ForeignKey(Profile,
                             verbose_name=_(u'użytkownik'),
                             editable=False,
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='user_changes')

    def __unicode__(self):
        return 'Zmiana na kranie %(tap_number)s: %(prev_beer)s -> %(new_beer)s @ %(time)s by %(user)s' % {
            'tap_number': self.tap.tap_number,
            'prev_beer': self.previous_beer.description() if self.previous_beer else u'∅',
            'new_beer': self.new_beer.description() if self.new_beer else u'∅',
            'time': self.timestamp,
            'user': self.user.email,
        }

    @classmethod
    def log(cls, tap, prev, new, profile=None):
        cls.objects.create(tap=tap, previous_beer=prev, new_beer=new, user=profile)

