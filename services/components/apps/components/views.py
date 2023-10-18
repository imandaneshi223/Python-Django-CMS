from rest_framework.viewsets import ModelViewSet

from .models import ComponentInstance, ComponentType
from .serializers import ComponentInstanceSerializer, ComponentTypeSerializer


class TypeView(ModelViewSet):
    serializer_class = ComponentTypeSerializer
    queryset = ComponentType.objects.all()


class ComponentView(ModelViewSet):
    serializer_class = ComponentInstanceSerializer
    queryset = ComponentInstance.objects.all()
