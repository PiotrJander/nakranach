from django.contrib import admin

from .models import *

@admin.register(Pub)
class PubAdmin(admin.ModelAdmin):
    pass

@admin.register(Tap)
class TapAdmin(admin.ModelAdmin):
    pass
