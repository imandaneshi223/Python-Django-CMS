import binascii
import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..services.models import ServicePermission


class IdentityToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='identity_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Identity Token")
        verbose_name_plural = _("Identity Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(IdentityToken, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class ElevatedToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='elevated_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Elevated Token")
        verbose_name_plural = _("Elevated Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ElevatedToken, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accepted_privacy_policy = models.BooleanField(default=False,
                                                  help_text='User accepted privacy policy')
    accepted_terms_of_service = models.BooleanField(default=False,
                                                    help_text='User accepted terms of service')
    is_registered = models.BooleanField(default=False,
                                        help_text='User was registered')
    date_registered = models.DateTimeField(default=None, null=True, editable=False)
    date_login = models.DateTimeField(default=None, null=True, editable=False)
    service_permissions = models.ManyToManyField(
        ServicePermission,
        verbose_name=_('Service permissions'),
        blank=True,
        help_text=_('Service permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )
