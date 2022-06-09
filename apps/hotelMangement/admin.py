from django.contrib import admin

# Register your models here.
from apps.hotelMangement.models import Hotel
from django.contrib.auth.models import Group


class CustomHotelAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_active',)
    list_filter = ('id', 'email', 'phone', 'is_active',)
    search_fields = ('id', 'email', 'phone')
    ordering = ('is_active', 'receive_newsletter')


#
admin.site.register(Hotel, CustomHotelAdmin)
# admin.site.register(Hotel)
admin.site.unregister(Group)
