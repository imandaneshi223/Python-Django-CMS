import os
from calendar import timegm
from datetime import datetime

import jwt
from django.db.models import Model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_encode_handler, jwt_decode_handler

from .serializers import CreateServiceJwtSerializer, ValidateServiceJwtSerializer


class StrictJWTAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if not jwt_value:
            raise AuthenticationFailed('No token!')
        try:
            payload = validate_service_jwt(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Signature has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding signature.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')
        except ValidationError:
            raise AuthenticationFailed('Malformed payload!!')
        return self.authenticate_credentials(payload)

    def authenticate_credentials(self, payload):
        return None, payload


def create_service_jwt_payload():
    from rest_framework_jwt.settings import api_settings
    payload = {}
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE
    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    serializer = CreateServiceJwtSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    return serializer.data


def create_service_jwt():
    return jwt_encode_handler(create_service_jwt_payload())


def validate_service_jwt(jwt):
    payload = jwt_decode_handler(jwt)
    serializer = ValidateServiceJwtSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    return payload


def get_service_name():
    if not os.environ.get('SERVICE_NAME'):
        raise ValidationError('Unknown service name!')
    return os.environ.get('SERVICE_NAME')


def get_service_permission(model=None, method=None):
    permission = [get_service_name(), model.__class__.__name__ if isinstance(model, Model) else None, method]
    return ':'.join([part for part in permission if part is not None])


def get_current_service_permissions():
    return list(map(lambda permission: permission.strip(' \t\n\r'), os.environ.get('SERVICE_PERMISSIONS').split(',')))
