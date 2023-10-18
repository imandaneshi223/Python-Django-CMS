import os
from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.utils import jwt_decode_handler, jwt_encode_handler

from .utils import create_service_jwt_payload, validate_service_jwt


class AuthenticationTest(TestCase):

    def test_create_service_jwt(self):
        jwt = jwt_encode_handler(create_service_jwt_payload())
        assert jwt
        payload = jwt_decode_handler(jwt)
        assert payload
        assert 'exp' in payload

    def test_create_service_jwt_fails_with_unknown_service_name(self):
        with patch.dict('os.environ', {'SERVICE_NAME': ''}):
            with self.assertRaises(ValidationError):
                jwt_encode_handler(create_service_jwt_payload())

    def test_create_service_jwt_returns_correct_data(self):
        payload = create_service_jwt_payload()
        assert 'exp' in payload
        assert 'service_name' in payload
        assert payload['service_name'] == os.environ['SERVICE_NAME']
        assert 'service_permissions' in payload
        assert isinstance(payload['service_permissions'], list)
        assert payload['is_service'] is True

    def test_validate_service_jwt_token(self):
        jwt = jwt_encode_handler(create_service_jwt_payload())
        validate_service_jwt(jwt)

    def test_validate_service_jwt_fails_with_invalid_data(self):
        with self.assertRaises(ValidationError):
            payload = create_service_jwt_payload()
            payload.pop('exp')
            jwt = jwt_encode_handler(payload)
            validate_service_jwt(jwt)
        with self.assertRaises(ValidationError):
            payload = create_service_jwt_payload()
            payload.pop('service_name')
            jwt = jwt_encode_handler(payload)
            validate_service_jwt(jwt)
        with self.assertRaises(ValidationError):
            payload = create_service_jwt_payload()
            payload.pop('service_permissions')
            jwt = jwt_encode_handler(payload)
            validate_service_jwt(jwt)
        with self.assertRaises(ValidationError):
            payload = create_service_jwt_payload()
            payload.pop('is_service')
            jwt = jwt_encode_handler(payload)
            validate_service_jwt(jwt)
