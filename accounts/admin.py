from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the CustomUser model.
    """
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'department')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_picture')}),
        (_('Employment info'), {'fields': ('department', 'position', 'hire_date', 'bio')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone', 'department'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
    filter_horizontal = ('groups', 'user_permissions',)

# Register the CustomUser model with the custom admin interface
admin.site.register(CustomUser, UserAdmin)
