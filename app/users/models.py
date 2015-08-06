# -*- coding: utf-8 -*-
import hashlib
import urllib
from django.contrib.auth import get_user_model

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from app.pubs.models import Pub


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    avatar_url = models.URLField(blank=True, null=True, max_length=1000)

    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)

    favorite_pubs = models.ManyToManyField(Pub, blank=True)
    # favorite_pubs = models.ManyToManyField(Pub, related_name='-')

    pubs = models.ManyToManyField(Pub, through='ProfilePub', related_name='employees', through_fields=('profile', 'pub'))

    def __unicode__(self):
        return unicode(self.user)

    @property
    def email(self):
        return self.user.email

    def fullname(self):
        """Returns name and surname concatenated. If these are empty, returns None"""
        if self.name or self.surname:
            return '%s %s' % (self.name, self.surname)
        else:
            None

    def role_descriptions(self):
        return [pp.role_desciption() for pp in self.profilepub_set.all()]

    def gravatar_url(self):
        """Returns the md5 hash of the email."""
        # default = 'http://americanmuslimconsumer.com/wp-content/uploads/2013/09/blank-user.jpg'
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.user.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': 'mm', 's': 90})
        # gravatar_url += urllib.urlencode({'s': 90})
        return gravatar_url

    @property
    def can_manage_pubs(self):
        return self.pubs.count() != 0
        # metoda Strucha, chyba nie do końca aktualna

    def is_admin(self):
        """
        Returns True if the user is a pub admin, ie. has the 'admin' role
        in at least one ProfilePub relationship.
        """
        return self.profilepub_set.filter(role='admin').exists()

    def managed_users(self):
        """
        Returns the list of workers in the managed pub.
        """
        if self.get_pub() and self.is_admin():
            return self.get_pub().employees.exclude(id=self.id).select_related('user')
        else:
            return []

    def get_pub(self):
        """
        Returns the pub associated with the user, or None.
        """
        try:
            return Pub.objects.get(profilepub__profile=self)
        except Pub.DoesNotExist:
            return None

    def is_in_pub(self):
        return bool(self.get_pub())

    def get_taps(self):
        pub = self.get_pub()
        if pub:
            return pub.taps.all()
        else:
            return None

    @classmethod
    def get_by_user(cls, user):
        """
        Returns the profile associated with given custom_user.
        Raises Profile.DoesNotExist if there is no associated profile.
        """
        return cls.objects.get(user=user.id)

    @classmethod
    def get_by_email(cls, email):
        user = get_user_model().objects.get(email=email)
        return user.profile

    @staticmethod
    def check_email_is_registered(email):
        """Checks if the given email is registered in Nakranach."""
        return get_user_model().objects.filter(email=email).exists()


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

    def __unicode__(self):
        entities = {'person': unicode(self.profile), 'role': self.get_role_display(), 'pub': unicode(self.pub), }
        return u'%(person)s pełni rolę %(role)s w %(pub)s' % entities

    def role_desciption(self):
        return '%s w pubie %s' % (self.get_role_display(), self.pub)

    @classmethod
    def get_role(cls, profile, pub):
        return cls.objects.get(profile=profile, pub=pub).get_role_display()

    @classmethod
    def remove_from_pub(cls, profile, pub):
        """Deletes the association between the profile and the pub."""
        cls.objects.filter(profile=profile, pub=pub).delete()

    @classmethod
    def change_role(cls, profile, pub, role):
        """Sets the new role for the user in the pub."""
        cls.objects.filter(profile=profile, pub=pub).update(role=role)
