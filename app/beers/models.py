# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Brewery(models.Model):
    name = models.CharField(verbose_name=_('nazwa'), max_length=255)
    country = models.CharField(verbose_name=_('kraj'), max_length=255)
