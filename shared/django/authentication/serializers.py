import os
from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, UUIDField, CharField, ListField, SerializerMethodField, BooleanField, \
    Field


class TimestampField(Field):
    def to_native(self, value):
        epoch = datetime(1970, 1, 1)
        return int((value - epoch).total_seconds())

    def to_internal_value(self, data):
        return data


class AbstractJwtSerializer(Serializer):
    exp = SerializerMethodField()
    is_user = SerializerMethodField()
    is_service = SerializerMethodField()

    def get_exp(self, obj):
        from rest_framework_jwt.settings import api_settings
        if 'exp' in obj:
            return obj['exp']
        return datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA

    def get_is_user(self, obj):
        return False

    def get_is_service(self, obj):
        return False


# TODO actually use it in Accounts service
class UserJwtSerializer(AbstractJwtSerializer):
    user_uuid = UUIDField(source='user_id')
    identity_token = CharField(max_length=40)
    elevated_token = CharField(max_length=40)
    user_permissions = ListField(child=CharField(max_length=120))
    service_permissions = ListField(child=CharField(max_length=120))
    is_loggedin = SerializerMethodField()

    def get_is_user(self, obj):
        return True

    @staticmethod
    def get_is_loggedin(obj):
        return obj.identity_token and obj.elevated_token


class CreateServiceJwtSerializer(AbstractJwtSerializer):
    service_name = SerializerMethodField()
    service_permissions = SerializerMethodField()

    def get_is_service(self, obj):
        return True

    def get_service_name(self, obj):
        if not os.environ.get('SERVICE_NAME'):
            raise ValidationError('Unknown service name!')
        return os.environ.get('SERVICE_NAME')

    def get_service_permissions(self, obj):
        if not os.environ.get('SERVICE_PERMISSIONS'):
            raise ValidationError('Unknown service permissions!')
        return list(
            map(lambda permission: permission.strip(' \t\n\r'), os.environ.get('SERVICE_PERMISSIONS').split(',')))


class ValidateServiceJwtSerializer(AbstractJwtSerializer):
    exp = TimestampField(required=True)
    service_name = CharField(max_length=120, required=True)
    service_permissions = ListField(required=True)
    is_service = BooleanField(required=True)
