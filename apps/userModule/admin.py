from django.contrib import admin
from .models import PhoneOTP
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(PhoneOTP)


class CustomUserAdmin(BaseUserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'phone', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Extradetails', {'fields': (
            'first_name', 'last_name', 'phone', 'date_joined', 'date_of_birth', 'address', 'city', 'country',
            'state', 'zipcode', 'role',
            'about_me', 'profile_image')})
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username','email','phone', 'password1', 'password2', 'is_staff', 'is_active')}
    #     ),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'date_of_birth', 'password1', 'password2')}
    #      ),
    # )
    search_fields = ('email',)
    ordering = ('email',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
