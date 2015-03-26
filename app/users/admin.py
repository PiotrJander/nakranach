# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ProfilePub

class ProfilePubInline(admin.StackedInline):
    model = ProfilePub
    extra = 0