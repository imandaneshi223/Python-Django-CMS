from django.urls import reverse
from rest_framework import status

from .utility import AccountsTestBase
from ..models import User


class UserEndpointsForAnonymousUserTest(AccountsTestBase):

    def get_tested_user(self):
        return self.registered_user

    def get_tested_user_password(self):
        return self.registered_user_password

    # create

    def test_create_is_allowed_without_authentication(self):
        self.assertEqual(status.HTTP_201_CREATED,
                         self.client.post(reverse('users'),
                                          format='json').status_code)

    def test_create_response_contains_identity_token(self):
        self.assertIsNotNone(self.client.post(reverse('users'),
                                              format='json').data['identity_token'])

    def test_create_user_was_created(self):
        count = User.objects.all().count()
        self.client.post(reverse('users'), format='json')
        self.assertEqual(count + 1, User.objects.all().count())

    def test_create_user_user_is_not_registered_after_creation(self):
        self.assertFalse(self.client.post(reverse('users'), format='json').data['is_registered'])

    # create/login

    def test_login_with_email_is_allowed_without_authentication(self):
        self.assertEqual(status.HTTP_200_OK,
                         self.client.post(reverse('users'),
                                          {'email': self.get_tested_user().email,
                                           'password': self.get_tested_user_password()},
                                          format='json').status_code)

    def test_login_with_email_returns_identity_token(self):
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'email': self.get_tested_user().email, 'password': self.get_tested_user_password()},
                             format='json').data['identity_token'])

    def test_login_with_email_returns_elevated_token(self):
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'email': self.get_tested_user().email, 'password': self.get_tested_user_password()},
                             format='json').data['elevated_token'])

    def test_login_with_email_fails_with_invalid_email(self):
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': 'invalid@email.com', 'password': self.get_tested_user_password()},
                                          format='json').status_code)

    def test_login_with_email_fails_with_invalid_password(self):
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': self.get_tested_user().email, 'password': 'invalid_password'},
                                          format='json').status_code)

    # retrieve

    def test_retrieve_by_uuid_is_forbidden_for_anonymous_user(self):
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_token_is_forbidden_for_anonymous_user(self):
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         self.client.get(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             format='json').status_code)

    # update

    def test_update_by_uuid_is_forbidden_for_anonymous_user(self):
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': 'new@email.com'},
                                           format='json').status_code)

    def test_update_by_token_is_forbidden_for_anonymous_user(self):
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email': 'new@email.com'},
                             format='json').status_code)

    def test_update_by_token_is_forbidden_for_anonymous_user_tmp(self):
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email': 'new@email.com'},
                             format='json').status_code)
