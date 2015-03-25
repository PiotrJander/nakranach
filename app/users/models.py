# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.pubs.models import Pub

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    avatar_url = models.URLField(blank=True, null=True, max_length=1000)

    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)

    favorite_pubs = models.ManyToManyField(Pub)

    pubs = models.ManyToManyField(Pub, through='ProfilePub', related_name='employees', through_fields=('profile', 'pub'))

    @property
    def can_manage_pubs(self):
        return self.pubs.count() != 0

    def __unicode__(self):
        return unicode(self.user)

class ProfilePub(models.Model):
    PUB_EMPLOYEE = 'employee'
    PUB_STOREMAN = 'storeman'
    PUB_ADMIN = 'admin'

    ROLE_CHOICES = (
        (PUB_EMPLOYEE, _(u'Pracownik baru')),
        (PUB_STOREMAN, _(u'Pracownik magazynu')),
        (PUB_ADMIN, _(u'Administrator'))
    )

    profile = models.ForeignKey(Profile, verbose_name=_(u'Użytkownik'))
    pub = models.ForeignKey(Pub, verbose_name=_(u'Pub'))
    role = models.CharField(max_length=20, verbose_name=_(u'Rola'), choices=ROLE_CHOICES)

    class Meta:
        verbose_name = _(u'profil-pub')
        verbose_name_plural = _(u'profile-puby')
        unique_together = ('profile', 'pub')