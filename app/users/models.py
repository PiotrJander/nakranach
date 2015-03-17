# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    avatar_url = models.URLField(blank=True, null=True, max_length=1000)