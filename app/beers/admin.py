from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Brewery)
admin.site.register(Style)
admin.site.register(Beer)
