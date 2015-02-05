# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Brewery(models.Model):
    class Meta:
        verbose_name = _('browar')
        verbose_name_plural = _('browary')

    name = models.CharField(verbose_name=_('nazwa'), max_length=255)
    country = models.CharField(verbose_name=_('kraj'), max_length=255)

class Style(models.Model):
    class Meta:
        verbose_name = _('styl')
        verbose_name_plural = _('style')

    name = models.CharField(verbose_name=_('nazwa'), max_length=255)

class Beer(models.Model):
    class Meta:
        verbose_name = _('piwo')
        verbose_name_plural = _('piwa')

    brewery = models.ForeignKey(Brewery, verbose_name=_('browar'))
    style = models.ForeignKey(Style,verbose_name=_('styl'))
    name = models.CharField(verbose_name=_('nazwa'), max_length=255)
    ibu = models.IntegerField(verbose_name=_('IBU'), blank=True, null=True)
    abv = models.DecimalField(verbose_name=_('ABV'), blank=True, null=True, decimal_places=1, max_digits=3)


