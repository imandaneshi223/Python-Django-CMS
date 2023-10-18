from django.db import models
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    name = models.SlugField(_("Name"), max_length=40, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class ServicePermission(models.Model):
    name = models.SlugField(_("Name"), max_length=40, primary_key=True)
    service = models.ForeignKey(
        Service, related_name='service_permission',
        on_delete=models.CASCADE, verbose_name=_("Service")
    )

    def __str__(self):
        return '{}.{}'.format(self.service.name, self.name)

    class Meta:
        verbose_name = _("Service permission")
        verbose_name_plural = _("Service permissions")
        unique_together = (('service', 'name'),)
