from django.contrib import admin

from .models import Site, Route


class SiteAdmin(admin.ModelAdmin):
    pass


class RouteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Site, SiteAdmin)
admin.site.register(Route, RouteAdmin)
