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

    def __unicode__(self):
        return self.name

class Style(models.Model):
    class Meta:
        verbose_name = _('styl')
        verbose_name_plural = _('style')

    name = models.CharField(verbose_name=_('nazwa'), max_length=255)

    def __unicode__(self):
        return self.name

class Beer(models.Model):
    class Meta:
        verbose_name = _('piwo')
        verbose_name_plural = _('piwa')

    # required
    brewery = models.ForeignKey(Brewery, verbose_name=_('browar'))
    style = models.ForeignKey(Style,verbose_name=_('styl'))
    name = models.CharField(verbose_name=_('nazwa'), max_length=255)

    # optional
    ibu = models.IntegerField(verbose_name=_('IBU'), blank=True, null=True)
    abv = models.DecimalField(verbose_name=_('ABV'), blank=True, null=True, decimal_places=1, max_digits=3)

    editable_fields = ['brewery', 'style', 'name', 'ibu', 'abv']

    def __unicode__(self):
        return self.name

    def description(self):
        return '%s %s' % (self.brewery.name, self.name)

    def export_form_data(self):
        """
        Returns a dictionary representing the ['brewery', 'style', 'name', 'ibu', 'abv'] fields of the instance.
        """
        return {k: unicode(getattr(self, k)) for k in self.editable_fields}
