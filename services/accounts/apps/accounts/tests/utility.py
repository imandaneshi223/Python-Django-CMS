import binascii
import os

from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from ..models import IdentityToken, ElevatedToken, User
from ...services.models import Service, ServicePermission


class AccountsTestBase(APITestCase):
    def get_tested_user(self):
        return NotImplementedError()

    def get_tested_user_password(self):
        return NotImplementedError()

    def get_tested_user_identity_token_key(self):
        return IdentityToken.objects.get(user=self.get_tested_user()).key

    def get_tested_user_elevated_token_key(self):
        return ElevatedToken.objects.get(user=self.get_tested_user()).key

    def authenticate_tested_user(self):
        self.authenticate_user(self.get_tested_user())

    def authenticate_tested_user_with_jwt(self):
        self.authenticate_user_with_jwt(self.get_tested_user())

    def login_and_authenticate_tested_user(self):
        self.login_user(self.get_tested_user())

    def login_and_authenticate_tested_user_with_jwt(self):
        self.login_user_with_jwt(self.get_tested_user())

    def authenticate_user(self, user):
        token = IdentityToken.objects.select_related('user').get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def authenticate_user_with_jwt(self, user):
        token = IdentityToken.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self._get_jwt_token(user, None))

    def login_user(self, user):
        token, created = ElevatedToken.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def login_user_with_jwt(self, user):
        elevated_token, created = ElevatedToken.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self._get_jwt_token(user, elevated_token.key))

    @staticmethod
    def generate_random_string():
        return binascii.hexlify(os.urandom(20)).decode()[:20]

    def setUp(self):
        self.anonymous_user = self._get_new_anonymous_user()
        self.authenticated_user = self._get_new_authenticated_user()

        self.registered_user_email = 'registered@email.com'
        self.registered_user_password = "registered_ran123domPaWORK"
        self.registered_user_first_name = 'John'
        self.registered_user_last_name = 'Doe'
        self.registered_user = self._get_new_registered_user(self.registered_user_email, self.registered_user_password,
                                                             self.registered_user_first_name,
                                                             self.registered_user_last_name)

        self.loggedin_user_password = "loggedin_ran123domPaWORK"
        self.loggedin_user_email = 'loggedin@email.com'
        self.loggedin_user_first_name = 'Paul'
        self.loggedin_user_last_name = 'Doe'
        self.loggedin_user = self._get_new_loggedin_user(self.loggedin_user_email, self.loggedin_user_password,
                                                         self.loggedin_user_first_name, self.loggedin_user_last_name)

    def _get_and_authenticate_new_anonymous_user(self):
        user = self._get_new_anonymous_user()
        token = IdentityToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user

    def _get_and_authenticate_new_registered_user(self):
        user = self._get_new_registered_user('{}@email.com'.format(self.generate_random_string()),
                                             self.generate_random_string(),
                                             'firstName{}'.format(self.generate_random_string()),
                                             'lastName{}'.format(self.generate_random_string()))
        token = IdentityToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user

    def _get_and_authenticate_new_logged_in_user(self):
        user = self._get_new_registered_user('{}@email.com'.format(self.generate_random_string()),
                                             self.generate_random_string(),
                                             'firstName{}'.format(self.generate_random_string()),
                                             'lastName{}'.format(self.generate_random_string()))
        IdentityToken.objects.create(user=user)
        elevated_token = ElevatedToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + elevated_token.key)
        return user

    def _get_new_authenticated_user(self):
        return IdentityToken.objects.create(
            user=User.objects.create(username='test_anonymous_{}'.format(self.generate_random_string()))).user

    def _get_new_anonymous_user(self):
        return User.objects.create(username='test_anonymous_{}'.format(self.generate_random_string()))

    def _get_new_registered_user(self, email, password, first_name, last_name):
        # register user
        user = self._get_new_authenticated_user()
        user.username = '{}{}{}'.format(first_name, last_name, self.generate_random_string())
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.accepted_privacy_policy = True
        user.accepted_terms_of_service = True
        user.is_registered = True
        user.date_registered = timezone.now()
        user.set_password(password)
        user.save()
        return user

    def _get_new_loggedin_user(self, email, password, first_name, last_name):
        # login user
        user = ElevatedToken.objects.create(
            user=self._get_new_registered_user(email, password, first_name, last_name)).user
        user.date_login = timezone.now()
        user.save()
        return user

    @staticmethod
    def _get_jwt_token(user, elevated_token=None):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        return jwt_encode_handler(jwt_payload_handler(user, elevated_token))

    @staticmethod
    def decode_jwt(jwt_value):
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        return jwt_decode_handler(jwt_value)

    @staticmethod
    def assign_and_return_service_permission_for_user(user, service_name='cms',
                                                      service_permission='view_public_content'):
        service, created = Service.objects.get_or_create(name=service_name)
        permission, created = ServicePermission.objects.get_or_create(name=service_permission, service=service)
        user.service_permissions.add(permission)
        return permission
