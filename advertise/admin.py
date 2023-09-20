from django.contrib import admin

from advertise.models import Advertise, AdvertiseImage


class AdvertiseImageInline(admin.TabularInline):
    model = AdvertiseImage


@admin.register(Advertise)
class AdvertiseAdmin(admin.ModelAdmin):
    inlines = [AdvertiseImageInline,]
    list_display = ['title', 'price', 'user', 'created']
    list_filter = ['price', 'created']
    ordering = ['created', 'price']


@admin.register(AdvertiseImage)
class AdvertiseImageAdmin(admin.ModelAdmin):
    list_display = ['advertise', 'image']
