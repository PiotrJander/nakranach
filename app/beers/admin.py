from django.contrib import admin

from .models import *

# Register your models here.

class BeerAdmin(admin.ModelAdmin):
    list_display = ['name', 'brewery', 'style']

admin.site.register(Brewery)
admin.site.register(Style)
admin.site.register(Beer, BeerAdmin)

