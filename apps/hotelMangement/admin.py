from django.contrib import admin

# Register your models here.
from apps.hotelMangement.models import Hotels
from django.contrib.auth.models import Group


class CustomHotelAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_active',)
    list_filter = ('id', 'email', 'phone', 'is_active',)
    search_fields = ('id', 'email', 'phone')
    ordering = ('is_active', 'receive_newsletter')


#
admin.site.register(Hotels, CustomHotelAdmin)
# admin.site.register(Hotels)
admin.site.unregister(Group)
