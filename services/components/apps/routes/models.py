import uuid

from django.db import models

from ..components.models import ComponentInstance


class Site(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    domain = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.domain


class Route(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    route = models.CharField(max_length=120)
    component = models.ForeignKey(ComponentInstance, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.site.domain, self.route)

    class Meta:
        unique_together = (('site', 'route'),)
