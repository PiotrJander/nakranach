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

    def fullname(self):
        """Returns name and surname concatenated."""
        return '%s %s' % (self.name, self.surname)

    def role_descs(self):
        """
        Returns a list of role descriptions. A role description is a string with information about the role
        and the pub. To be used in contexts where the user is known implicitly
        and we don't want to include the user explicitly.
        """
        return [profile_pub.role_desc() for profile_pub in ProfilePub.objects.filter(profile=self)]

    @property
    def can_manage_pubs(self):
        return self.pubs.count() != 0

    def can_manage_users(self):
        """
        Returns True if the user is a pub admin, ie. has the 'admin' role
        in at least one ProfilePub relationship.
        """
        return ProfilePub.objects.filter(profile=self, role='admin').count() > 0

    def managed_users(self):
        """
        Returns the list of users that the user can manage.
        """
        return Profile.objects.raw("""
        SELECT user.* from
        users_profile as admin,
        users_profile as user,
        users_profilepub as pp1,
        users_profilepub as pp2,
        pubs_pub as pub
        where admin.id = %(user_id)s and admin.id = pp1.profile_id and pp1.role = 'admin'
        and pp1.pub_id = pub.id and pub.id = pp2.pub_id and pp2.profile_id = user.id;
        """, {'user_id': self.id})

    @staticmethod
    def get_by_user(user):
        """
        Returns the profile associated with given custom_user.
        Raises Profile.DoesNotExist if there is no associated profile.
        """
        return Profile.objects.get(user=user.id)

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
        return '%s w %s' % (self.get_role_display(), unicode(self.pub))

    class Meta:
        verbose_name = _(u'profil-pub')
        verbose_name_plural = _(u'profile-puby')
        unique_together = ('profile', 'pub')
