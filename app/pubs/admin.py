from django.contrib import admin

from .models import *

from app.users.admin import ProfilePubInline
from django.utils import timezone

class VolumeAdminInline(admin.StackedInline):
    model = Volume
    extra = 0

class WaitinBeerAdminInline(admin.StackedInline):
    model = WaitingBeer
    extra = 0

class TapAdminInline(admin.StackedInline):
    model = Tap
    extra = 0

@admin.register(Pub)
class PubAdmin(admin.ModelAdmin):
    inlines = (VolumeAdminInline, TapAdminInline, WaitinBeerAdminInline, ProfilePubInline)

    def save_model(self, request, obj, form, change):
        if 'avatar' in form.changed_data:
            obj.avatar_timestamp = timezone.now()

        super(PubAdmin, self).save_model(request, obj, form, change)

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

class PriceAdminBeerInline(PriceAdminInline):
    exclude = ['tap',]

class PriceAdminTapInline(PriceAdminInline):
    exclude = ['beer',]

class PriceOwnerAdmin(admin.ModelAdmin):
    price_class = PriceAdminInline

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(PriceOwnerAdmin, self).get_form(request, obj, **kwargs)

    def add_view(self, *args, **kwargs):
        self.inlines = ()
        return super(PriceOwnerAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = (self.price_class,)
        return super(PriceOwnerAdmin, self).change_view(*args, **kwargs)

@admin.register(Tap)
class TapAdmin(PriceOwnerAdmin):
    price_class = PriceAdminTapInline

@admin.register(WaitingBeer)
class WaitingBeerAdmin(PriceOwnerAdmin):
    price_class = PriceAdminBeerInline