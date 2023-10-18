from django.contrib import admin

from .models import ComponentType, ComponentInstance


class ComponentTypeAdmin(admin.ModelAdmin):
    pass


class ComponentInstanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(ComponentType, ComponentTypeAdmin)
admin.site.register(ComponentInstance, ComponentInstanceAdmin)

