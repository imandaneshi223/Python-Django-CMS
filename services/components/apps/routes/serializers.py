from rest_framework.serializers import ModelSerializer, UUIDField

from .models import Site, Route


class SiteSerializer(ModelSerializer):
    id = UUIDField(read_only=True)

    class Meta:
        model = Site
        fields = ('id', 'domain')


class RouteSerializer(ModelSerializer):
    id = UUIDField(read_only=True)

    class Meta:
        model = Route
        fields = ('id', 'route', 'site', 'component')
