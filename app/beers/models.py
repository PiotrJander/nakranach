# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from app.main.utils import normalize_for_search


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

    # automatic
    search = models.CharField(editable=False, max_length=511)

    editable_fields = ['brewery', 'style', 'name', 'ibu', 'abv']

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.search = normalize_for_search(self.brewery.name + ' ' + self.name)
        super(Beer, self).save(force_insert, force_update, using, update_fields)

    def description(self):
        return '%s %s' % (self.brewery.name, self.name)

    def export_form_data(self):
        """
        Returns a dictionary representing the ['brewery', 'style', 'name', 'ibu', 'abv'] fields of the instance.
        """
        return {k: unicode(getattr(self, k)) for k in self.editable_fields}

    def secondary_data(self):
        """
        Returns a string which consists of concatenated: ``style``, ``ibu``, ``abv``.
        """
        if self.ibu and self.abv:
            return '%s, %d IBU, %.1f%% ABV' % (self.style.name, self.ibu, self.abv)
        elif self.ibu:
            return '%s, %d IBU' % (self.style.name, self.ibu)
        elif self.abv:
            return '%s, %.1f%% ABV' % (self.style.name, self.abv)
        else:
            return '%s' % self.style.name

    def search_dict(self):
        """
        Returns a dictionary representation of ``name``, ``brewery.name`` as "brewery", and ``secondary_data``.
        """
        return {
            'id': self.id,
            'name': self.name,
            'brewery': self.brewery.name,
            'secondary_data': self.secondary_data(),
            'text': self.description(),
        }

    @classmethod
    def match(cls, search_string):
        """
        Returns a ``QuerySet`` of ``Beer``s whose search field matches contains the ``search string``.

        ``search_string`` is normalized in the first place.
        """
        normalized = normalize_for_search(search_string)
        return cls.objects.filter(search__contains=normalized)