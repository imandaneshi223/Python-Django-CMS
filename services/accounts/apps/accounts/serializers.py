from django.utils import timezone
from rest_framework.serializers import ModelSerializer, SerializerMethodField, BooleanField, ValidationError, EmailField
from rest_framework_jwt.settings import api_settings

from .authorization import is_loggedin, get_user_permissions_string_list, get_user_service_permissions_string_list
from .models import User, IdentityToken, ElevatedToken


class UserSerializer(ModelSerializer):
    identity_token = SerializerMethodField(read_only=True)
    elevated_token = SerializerMethodField(read_only=True)
    jwt_token = SerializerMethodField(read_only=True)
    user_permissions = SerializerMethodField(read_only=True)
    service_permissions = SerializerMethodField(read_only=True)
    accepted_terms_of_service = BooleanField()
    accepted_privacy_policy = BooleanField()
    is_registered = BooleanField()
    email = EmailField(allow_blank=True)

    def get_identity_token(self, instance):
        if 'identity_token' in self.context:
            return self.context['identity_token'].key
        token, created = IdentityToken.objects.get_or_create(user=instance)
        return token.key

    def get_elevated_token(self, instance):
        if is_loggedin(self.context['request']):
            try:
                return ElevatedToken.objects.get(user=instance).key
            except ElevatedToken.DoesNotExist:
                return None
        return None

    def get_jwt_token(self, instance):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        if is_loggedin(self.context['request']):
            return jwt_encode_handler(jwt_payload_handler(instance, ElevatedToken.objects.get(user=instance).key))
        return jwt_encode_handler(jwt_payload_handler(instance, None))

    @staticmethod
    def get_user_permissions(instance):
        return get_user_permissions_string_list(instance)

    @staticmethod
    def get_service_permissions(instance):
        return get_user_service_permissions_string_list(instance)

    def validate_email(self, value):
        if value == self.context['request'].user.email:
            return value
        if User.objects.filter(email=value).exists():
            raise ValidationError('Not unique email!')
        return value

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'identity_token', 'elevated_token', 'jwt_token',
            'user_permissions', 'service_permissions', 'is_registered', 'accepted_privacy_policy',
            'accepted_terms_of_service')
        read_only_fields = (
            'id', 'username', 'identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'user_permissions',
            'service_permissions')


class AuthenticatedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'identity_token', 'elevated_token', 'jwt_token', 'email', 'is_registered', 'accepted_privacy_policy',
            'accepted_terms_of_service')
        read_only_fields = ('identity_token', 'elevated_token', 'jwt_token', 'is_registered')


class AuthorizedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'identity_token', 'elevated_token', 'jwt_token',
            'user_permissions', 'service_permissions', 'is_registered', 'accepted_privacy_policy',
            'accepted_terms_of_service')
        read_only_fields = (
            'id', 'username', 'identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'username',
            'first_name', 'last_name', 'user_permissions', 'service_permissions')


class CreateUserSerializer(UserSerializer):

    def get_identity_token(self, instance):
        identity_token, created = IdentityToken.objects.get_or_create(user=instance)
        return identity_token.key

    class Meta:
        model = User
        fields = ('identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'accepted_privacy_policy',
                  'accepted_terms_of_service')
        read_only_fields = ('identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'accepted_privacy_policy',
                            'accepted_terms_of_service')


class CollectEmailSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'accepted_privacy_policy',
                  'accepted_terms_of_service')
        read_only_fields = ('identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'accepted_privacy_policy',
                            'accepted_terms_of_service')
        extra_kwargs = {
            'email': {'write_only': True}
        }


class AcceptPrivacyPolicySerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'accepted_privacy_policy',
                  'accepted_terms_of_service')
        read_only_fields = ('identity_token', 'elevated_token', 'jwt_token', 'is_registered',
                            'accepted_terms_of_service')


class LoginUserSerializer(UserSerializer):

    def get_elevated_token(self, instance):
        elevated_token, created = ElevatedToken.objects.get_or_create(user=instance)
        return elevated_token.key

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.date_login = timezone.now()
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('email', 'password', 'identity_token', 'elevated_token', 'jwt_token', 'is_registered',
                  'accepted_privacy_policy', 'accepted_terms_of_service')
        read_only_fields = ('identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'accepted_privacy_policy',
                            'accepted_terms_of_service')
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True}
        }


class RegisterUserSerializer(UserSerializer):

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data.get('password'))
        instance.is_registered = True
        instance.date_registered = timezone.now()
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'identity_token', 'elevated_token', 'jwt_token',
                  'is_registered', 'accepted_privacy_policy', 'accepted_terms_of_service', 'date_registered')
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True}
        }
