from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from .models import User, ElevatedToken, IdentityToken


class AccountsUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_registered', 'is_staff', 'is_superuser', 'accepted_privacy_policy',
            'accepted_terms_of_service', 'groups', 'user_permissions', 'service_permissions'
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'service_permissions')


class IdentityTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


class ElevatedTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


admin.site.register(ElevatedToken, ElevatedTokenAdmin)
admin.site.register(IdentityToken, IdentityTokenAdmin)
admin.site.register(Permission)
admin.site.register(User, AccountsUserAdmin)
