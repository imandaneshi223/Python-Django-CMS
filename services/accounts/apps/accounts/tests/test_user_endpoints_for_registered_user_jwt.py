from django.urls import reverse

from .test_user_endpoints_for_registered_user import UserEndpointsForRegisteredUserTest


class UserEndpointsForRegisteredUserAuthenticatedByJwtTest(UserEndpointsForRegisteredUserTest):
    def authenticate_tested_user(self):
        self.authenticate_tested_user_with_jwt()

    def login_and_authenticate_tested_user(self):
        self.login_and_authenticate_tested_user_with_jwt()

    def test_retrieve_by_uuid_response_contains_jwt_with_service_permissions(self):
        self.login_and_authenticate_tested_user()
        service_permission = self.assign_and_return_service_permission_for_user(self.get_tested_user())
        jwt_payload = self.decode_jwt(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                                      format='json').data['jwt_token'])
        self.assertEqual(str(service_permission),
                         jwt_payload['service_permissions'][0])

    def test_retrieve_by_token_response_contains_jwt_with_service_permissions(self):
        self.login_and_authenticate_tested_user()
        service_permission = self.assign_and_return_service_permission_for_user(self.get_tested_user())
        jwt_payload = self.decode_jwt(self.client.get(
            reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
            format='json').data['jwt_token'])
        self.assertEqual(str(service_permission),
                         jwt_payload['service_permissions'][0])
