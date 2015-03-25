from django.contrib import admin

from .models import *

from app.users.admin import ProfilePubInline

class VolumeAdminInline(admin.StackedInline):
    model = Volume

@admin.register(Pub)
class PubAdmin(admin.ModelAdmin):
    inlines = (VolumeAdminInline, ProfilePubInline)

class PriceAdminInline(admin.TabularInline):
    model = Price

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PriceAdminInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'volume':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(pub=request._obj_.pub)
            else:
                field.queryset = field.queryset.none()

        return field

@admin.register(Tap)
class TapAdmin(admin.ModelAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = ()
        return super(TapAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = (PriceAdminInline,)
        return super(TapAdmin, self).change_view(*args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(TapAdmin, self).get_form(request, obj, **kwargs)
