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

    favorite_pubs = models.ManyToManyField(Pub)
    # favorite_pubs = models.ManyToManyField(Pub, related_name='-')

    pubs = models.ManyToManyField(Pub, through='ProfilePub', related_name='employees', through_fields=('profile', 'pub'))

    def fullname(self):
        """Returns name and surname concatenated. If these are empty, return the email."""
        if self.name or self.surname:
            return '%s %s' % (self.name, self.surname)
        else:
            return self.user.email

    def role_descs(self):
        """
        Returns a list of role descriptions. A role description is a string with information about the role
        and the pub. To be used in contexts where the user is known implicitly
        and we don't want to include the user explicitly.
        """
        return [profile_pub.role_desc() for profile_pub in ProfilePub.objects.filter(profile=self)]

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

    def is_admin(self):
        """
        Returns True if the user is a pub admin, ie. has the 'admin' role
        in at least one ProfilePub relationship.
        """
        return ProfilePub.objects.filter(profile=self, role='admin')

    def managed_users(self):
        """
        Returns the list of workers in the managed pub.
        """
        if self.managed_pub():
            return self.managed_pub().employees.all()
        else:
            return []

    # def managed_users(self):
    #     """
    #     Returns the list of users that the user can manage.
    #     """
    #     return Profile.objects.raw("""
    #     SELECT user.* from
    #     users_profile as admin,
    #     users_profile as user,
    #     users_profilepub as pp1,
    #     users_profilepub as pp2,
    #     pubs_pub as pub
    #     where admin.id = %(user_id)s and admin.id = pp1.profile_id and pp1.role = 'admin'
    #     and pp1.pub_id = pub.id and pub.id = pp2.pub_id and pp2.profile_id = user.id;
    #     """, {'user_id': self.id})

    def managed_pub(self):
        """
        Returns the pub managed by the user, or None is the user is not an admin.

        CRUCIAL: assumes that a single user can only manage one pub, which is not enforced by code however
        """
        try:
            return Pub.objects.get(profilepub__profile=self, profilepub__role='admin')
        except Pub.DoesNotExist:
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
        return cls.get_by_user(user)

    @classmethod
    def associated_with_pub(cls, pub):
        "Returns an iterable of profiles associated with the given pub."
        return cls.objects.filter(pub=pub)

    @staticmethod
    def check_email_is_registered(email):
        """Checks if the given email is registered in Nakranach."""
        return email in (user.email for user in get_user_model().objects.all())

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

    def __unicode__(self):
        entities = {'person': unicode(self.profile), 'role': self.get_role_display(), 'pub': unicode(self.pub), }
        return u'%(person)s pełni rolę %(role)s w %(pub)s' % entities

    def role_desc(self):
        """
        Returns a string with information about the role and the pub. To be used in contexts where the user
        is known implicitly and we don't want to include the user explicitly.
        """
        return '%s w pubie %s' % (self.get_role_display(), unicode(self.pub))

    @classmethod
    def remove_from_pub(cls, profile, pub):
        """Deletes the association between the profile and the pub."""
        cls.objects.filter(profile=profile, pub=pub).delete()

    @classmethod
    def change_role(cls, profile, pub, role):
        """Sets the new role for the user in the pub."""
        cls.objects.filter(profile=profile, pub=pub).update(role=role)

    class Meta:
        verbose_name = _(u'profil-pub')
        verbose_name_plural = _(u'profile-puby')
        unique_together = ('profile', 'pub')
