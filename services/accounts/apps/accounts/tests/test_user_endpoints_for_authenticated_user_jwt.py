from .test_user_endpoints_for_authenticated_user import UserEndpointsForAuthenticatedUserTest


class UserEndpointsForAuthenticatedUserAuthenticatedByJwtTest(UserEndpointsForAuthenticatedUserTest):
    def authenticate_tested_user(self):
        self.authenticate_tested_user_with_jwt()

    def login_and_authenticate_tested_user(self):
        self.login_and_authenticate_tested_user_with_jwt()
