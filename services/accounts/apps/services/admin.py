from django.contrib import admin

from .models import Service, ServicePermission


class ServiceAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + tuple([item.name for item in obj._meta.fields])
        return self.readonly_fields


class ServicePermissionAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + tuple([item.name for item in obj._meta.fields])
        return self.readonly_fields


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServicePermission, ServicePermissionAdmin)
