from django.urls import reverse
from rest_framework import status

from .utility import AccountsTestBase
from ..models import ElevatedToken


class UserEndpointsForAuthenticatedUserTest(AccountsTestBase):

    def get_tested_user(self):
        return self.authenticated_user

    def get_tested_user_password(self):
        return None

    # retrieve by uuid

    def test_retrieve_by_uuid_user_can_retrieve_itself(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_returns_identity_token(self):
        self.authenticate_tested_user()
        self.assertIsNotNone(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                             format='json').data['identity_token'])

    def test_retrieve_by_uuid_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    # retrieve by token

    def test_retrieve_by_token_user_can_retrieve_itself(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             format='json').status_code)

    def test_retrieve_by_token_returns_identity_token(self):
        self.authenticate_tested_user()
        self.assertIsNotNone(
            self.client.get(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                            format='json').data['identity_token'])

    def test_retrieve_by_token_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-token',
                                                 args=(ElevatedToken.objects.get(user=self.loggedin_user).key,)),
                                         format='json').status_code)

    # update by uuid

    def test_update_by_uuid_user_cannot_update_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                           {'email': 'new@email.com'},
                                           format='json').status_code)

    def test_update_by_uuid_user_can_update_own_email_if_he_accepted_privacy_policy(self):
        new_email = 'new@email.com'
        self.get_tested_user().accepted_privacy_policy = True
        self.get_tested_user().save()
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': new_email},
                                           format='json').status_code)
        self.get_tested_user().refresh_from_db()
        self.assertEqual(new_email, self.get_tested_user().email)

    def test_update_by_uuid_user_cannot_update_own_email_if_he_did_not_accepted_privacy_policy(self):
        self.get_tested_user().accepted_privacy_policy = False
        self.get_tested_user().save()
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': 'new@email.com'},
                                           format='json').status_code)

    def test_update_by_uuid_user_updates_privacy_policy(self):
        new_accepted_privacy_policy = True
        self.authenticate_tested_user()
        self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                          {'accepted_privacy_policy': new_accepted_privacy_policy},
                          format='json')
        self.get_tested_user().refresh_from_db()
        self.assertEqual(new_accepted_privacy_policy, self.get_tested_user().accepted_privacy_policy)

    def test_update_by_uuid_user_cannot_update_anything_privacy_policy(self):
        new_username = 'new-username'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'username': new_username},
                                           format='json').status_code)

    # update by token

    def test_update_by_token_user_cannot_update_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-token',
                                                   args=(ElevatedToken.objects.get(user=self.loggedin_user).key,)),
                                           {'email': 'new@email.com'},
                                           format='json').status_code)

    def test_update_by_token_user_can_update_own_privacy_policy(self):
        new_accepted_privacy_policy = True
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'accepted_privacy_policy': new_accepted_privacy_policy},
                             format='json').status_code)

    def test_update_by_token_updates_privacy_policy(self):
        new_accepted_privacy_policy = True
        self.authenticate_tested_user()
        self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                          {'accepted_privacy_policy': new_accepted_privacy_policy},
                          format='json')
        self.get_tested_user().refresh_from_db()
        self.assertEqual(new_accepted_privacy_policy, self.get_tested_user().accepted_privacy_policy)

    def test_update_by_token_user_cannot_update_anything_but_email_and_privacy_policy(self):
        new_username = 'new-username'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'username': new_username},
                             format='json').status_code)

    # update/register by uuid

    def test_update_by_uuid_with_values_required_by_registration_sets_registered_flag(self):
        self.authenticate_tested_user()
        self.assertTrue(self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                          data={'username': 'test', 'email': 'test@test.net',
                                                'password': 'password', 'accepted_privacy_policy': True,
                                                'accepted_terms_of_service': True},
                                          format='json').data['is_registered'])

    # update/register by token

    def test_update_by_token_with_values_required_by_registration_sets_registered_flag(self):
        self.authenticate_tested_user()
        self.assertTrue(
            self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                              data={'email': 'test@test.net', 'password': 'password', 'accepted_privacy_policy': True,
                                    'accepted_terms_of_service': True},
                              format='json').data['is_registered'])

    def test_update_by_token_with_values_required_by_registration_sets_accepted_terms_of_service_flag(self):
        self.authenticate_tested_user()
        self.assertTrue(
            self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                              data={'email': 'test@test.net', 'password': 'password', 'accepted_privacy_policy': True,
                                    'accepted_terms_of_service': True},
                              format='json').data['accepted_terms_of_service'])

    def test_update_by_token_with_values_required_by_registration_updates_email(self):
        new_email = 'test@test.net'
        self.authenticate_tested_user()
        self.assertEqual(
            new_email,
            self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                              data={'email': new_email, 'password': 'password', 'accepted_privacy_policy': True,
                                    'accepted_terms_of_service': True},
                              format='json').data['email'])
        self.get_tested_user().refresh_from_db()
        self.assertEqual(new_email, self.get_tested_user().email)
