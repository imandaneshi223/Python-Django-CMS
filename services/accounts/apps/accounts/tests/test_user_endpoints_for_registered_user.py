from django.urls import reverse
from rest_framework import status

from .utility import AccountsTestBase
from ..models import ElevatedToken, IdentityToken


class UserEndpointsForRegisteredUserTest(AccountsTestBase):

    def get_tested_user(self):
        return self.registered_user

    def get_tested_user_password(self):
        return self.registered_user_password

    # retrieve by uuid

    def test_retrieve_by_uuid_user_can_retrieve_itself_if_logged_in(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_user_can_retrieve_itself_if_logged_in_and_response_will_contain_elevated_token(self):
        self.login_and_authenticate_tested_user()
        self.assertIsNotNone(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                             format='json').data['elevated_token'])

    def test_retrieve_by_uuid_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_loggedin_user_cannot_retrieve_other_user(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    # retrieve by token

    def test_retrieve_by_token_user_can_retrieve_itself_if_logged_in(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(
                             reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                             format='json').status_code)

    def test_retrieve_by_token_user_can_retrieve_itself_if_logged_in_and_response_will_contain_elevated_token(self):
        self.login_and_authenticate_tested_user()
        self.assertIsNotNone(
            self.client.get(reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                            format='json').data['elevated_token'])

    def test_retrieve_by_token_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-token',
                                                 args=(IdentityToken.objects.get(user=self.loggedin_user).key,)),
                                         format='json').status_code)

    def test_retrieve_by_token_loggedin_user_cannot_retrieve_other_user(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-token',
                                                 args=(ElevatedToken.objects.get(user=self.loggedin_user).key,)),
                                         format='json').status_code)

    # update by uuid

    def test_update_by_uuid_is_forbidden_for_registered_user_if_not_logged_in(self):
        new_email = 'new@email.com'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': new_email},
                                           format='json').status_code)

    def test_update_by_uuid_is_allowed_for_registered_user_logged_in(self):
        new_email = 'new@email.com'
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': new_email},
                                           format='json').status_code)

    def test_update_by_uuid_user_can_update_own_email_with_already_set_email(self):
        user = self.get_tested_user()
        user.email = 'test@email.com'
        user.save()
        user.refresh_from_db()
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': user.email},
                                           format='json').status_code)

    def test_update_by_uuid_rejects_duplicated_emails(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_400_BAD_REQUEST,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': self.loggedin_user_email, 'accepted_privacy_policy': True},
                                           format='json').status_code)

    # update by token

    def test_update_by_token_is_forbidden_for_registered_user_if_not_logged_in(self):
        new_email = 'new@email.com'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email': new_email},
                             format='json').status_code)

    def test_update_by_token_is_allowed_for_registered_user_logged_in(self):
        new_email = 'new@email.com'
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                             {'email': new_email},
                             format='json').status_code)

    def test_update_by_token_user_can_update_own_email_with_already_set_email(self):
        user = self.get_tested_user()
        user.email = 'test@email.com'
        user.save()
        user.refresh_from_db()
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email': user.email},
                             format='json').status_code)

    def test_update_by_token_rejects_duplicated_emails(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_400_BAD_REQUEST,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email': self.loggedin_user_email, 'accepted_privacy_policy': True},
                             format='json').status_code)

    # destroy by uuid

    def test_destroy_by_uuid_logs_user_out(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(1, ElevatedToken.objects.filter(user=self.get_tested_user()).count())
        self.client.delete(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)), format='json')
        self.assertEqual(0, ElevatedToken.objects.filter(user=self.get_tested_user()).count())

    # destroy by token

    def test_destroy_by_token_logs_user_out(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(1, ElevatedToken.objects.filter(user=self.get_tested_user()).count())
        self.client.delete(reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                           format='json')
        self.assertEqual(0, ElevatedToken.objects.filter(user=self.get_tested_user()).count())

    # create/login

    def test_login_with_email_returns_identity_token(self):
        self.authenticate_tested_user()
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'email': self.get_tested_user().email, 'password': self.get_tested_user_password()},
                             format='json').data['identity_token'])

    def test_login_with_email_returns_elevated_token(self):
        self.authenticate_tested_user()
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'email': self.get_tested_user().email, 'password': self.get_tested_user_password()},
                             format='json').data['elevated_token'])

    def test_login_with_email_fails_with_invalid_email(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': 'invalid@email.com', 'password': self.get_tested_user_password()},
                                          format='json').status_code)

    def test_login_with_email_fails_with_invalid_password(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': self.get_tested_user().email, 'password': 'invalid_password'},
                                          format='json').status_code)

    def test_login_is_forbidden_if_user_is_not_registered(self):
        user = self.get_tested_user()
        user.is_registered = False
        user.save()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': user.email,
                                           'password': self.get_tested_user_password()},
                                          format='json').status_code)
