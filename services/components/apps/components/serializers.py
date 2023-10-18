from rest_framework.serializers import ModelSerializer, UUIDField

from .models import ComponentInstance, ComponentType


class ComponentInstanceSerializer(ModelSerializer):
    id = UUIDField(read_only=True)

    class Meta:
        model = ComponentInstance
        fields = ('id', 'children', 'type', 'name')


class ComponentTypeSerializer(ModelSerializer):
    id = UUIDField(read_only=True)

    class Meta:
        model = ComponentType
        fields = ('id', 'name')
