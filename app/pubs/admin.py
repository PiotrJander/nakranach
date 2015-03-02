from django.contrib import admin

from .models import *

class VolumeAdminInline(admin.StackedInline):
    model = Volume

@admin.register(Pub)
class PubAdmin(admin.ModelAdmin):
    inlines = (VolumeAdminInline,)

@admin.register(Tap)
class TapAdmin(admin.ModelAdmin):
    pass
