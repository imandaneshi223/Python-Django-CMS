import uuid

from django.db import models


class AbstractComponentType(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True, blank=False, null=False)

    class Meta:
        abstract = True


class ComponentType(AbstractComponentType):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Component type'
        verbose_name_plural = 'Component type'


class AbstractComponentInstance(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(ComponentType, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ComponentInstance(AbstractComponentInstance):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        if self.name:
            return '{}:{}'.format(self.type.name, self.name)
        return self.name or '{}:{}'.format(self.type.name, self.id)

    class Meta:
        verbose_name = 'Component instance'
        verbose_name_plural = 'Component instances'
