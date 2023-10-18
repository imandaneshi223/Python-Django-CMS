import jwt
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_payload_handler, jwt_decode_handler

from .authorization import get_user_permissions_string_list, get_user_service_permissions_string_list
from .models import ElevatedToken, IdentityToken, User


def user_jwt_payload_handler(user, elevated_token=None):
    payload = jwt_payload_handler(user)
    payload.pop('username')
    payload.pop('email')

    try:
        payload['identity_token'] = IdentityToken.objects.get(user=user).key
    except IdentityToken.DoesNotExist:
        raise AuthenticationFailed('Identity token does not exist!')

    payload['elevated_token'] = elevated_token
    payload['user_permissions'] = get_user_permissions_string_list(user)
    payload['service_permissions'] = get_user_service_permissions_string_list(user)
    return payload


class JWTAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Signature has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding signature.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed()

        return self.authenticate_credentials(payload)

    def authenticate_credentials(self, payload):
        try:
            user = IdentityToken.objects.select_related('user').get(key=payload['identity_token']).user
        except IdentityToken.DoesNotExist:
            raise AuthenticationFailed('No valid token in JWT payload!')
        except User.DoesNotExist:
            raise AuthenticationFailed('No valid token in JWT payload!')
        if not user.is_active:
            raise AuthenticationFailed('User account is disabled.')
        return user, payload


class ElevatedTokenAuthentication(TokenAuthentication):
    def get_model(self):
        return ElevatedToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            return None

        if not token.user.is_active:
            return None

        return token.user, token


class IdentityTokenAuthentication(TokenAuthentication):
    def get_model(self):
        return IdentityToken
