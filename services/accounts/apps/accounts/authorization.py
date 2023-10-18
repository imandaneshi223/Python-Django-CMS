from django.contrib.auth.models import Permission
from django.utils.text import slugify
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_jwt.settings import api_settings

from .models import User, IdentityToken, ElevatedToken

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def get_user_permissions_string_list(user):
    def get_unique_permissions_list(permissions_set):
        return list(set(['{}.{}.{}'.format(slugify(perm.content_type.app_label).replace('-', '_'),
                                           slugify(perm.content_type).replace('-', '_'),
                                           slugify(perm.codename).replace('-', '_')) for perm in permissions_set]))

    return get_unique_permissions_list(
        user.user_permissions.all() | Permission.objects.filter(group__user=user))


def get_user_service_permissions_string_list(user):
    return [str(perm) for perm in user.service_permissions.all()]


def is_authenticated(request=None):
    if request is None or not isinstance(request, Request) or not isinstance(request.user, User):
        return False
    if isinstance(request.auth, IdentityToken):
        try:
            return request.auth == IdentityToken.objects.get(user=request.user)
        except IdentityToken.DoesNotExist:
            return False
    if isinstance(request.auth, ElevatedToken):
        try:
            return request.auth == ElevatedToken.objects.get(user=request.user)
        except ElevatedToken.DoesNotExist:
            return False
    if isinstance(request.auth, dict):
        try:
            return request.auth['identity_token'] == IdentityToken.objects.get(user=request.user).key
        except IdentityToken.DoesNotExist:
            return False
    return False


def is_registered(request=None):
    return is_authenticated(request) and request.user.is_registered


def is_loggedin(request=None):
    if not is_registered(request):
        return False
    if isinstance(request.auth, ElevatedToken):
        return True
    if not isinstance(request.auth, dict) or 'elevated_token' not in request.auth or not request.auth['elevated_token']:
        return False
    try:
        ElevatedToken.objects.get(key=request.auth['elevated_token'])
        return True
    except ElevatedToken.DoesNotExist:
        return False


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return is_authenticated(request)


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return is_authenticated(request)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User) and obj == request.user:
            return True
        return False


class IsLoggedInOwner(IsOwner):

    def has_permission(self, request, view):
        if is_loggedin(request):
            return True
        if is_registered(request):
            return False
        return is_authenticated(request)
