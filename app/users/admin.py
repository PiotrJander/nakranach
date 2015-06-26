# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ProfilePub, Profile

class ProfilePubInline(admin.StackedInline):
    model = ProfilePub
    extra = 0

admin.site.register(ProfilePub)
admin.site.register(Profile)
