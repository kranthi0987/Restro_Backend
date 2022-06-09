from django.contrib import admin

# Register your models here.
from apps.manageMenu.models import Menu, Item, SubMenu


class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_price', 'item_image', 'is_active')
    list_filter = ('item_name', 'item_price', 'item_image', 'is_active')
    search_fields = ('item_name', 'item_price',)
    ordering = ('is_active', 'item_price')


#
admin.site.register(Item, CustomItemAdmin)
admin.site.register(Menu)
admin.site.register(SubMenu)
