from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import ComponentInstance, ComponentType
from lib.authentication.utils import create_service_jwt, get_current_service_permissions


class ComponentTypeTest(APITestCase):

    def authenticate_by_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + create_service_jwt())

    def setUp(self):
        assert 'components:ComponentType:GET' in get_current_service_permissions()
        self.authenticate_by_jwt()
        self.type = ComponentType.objects.create(name='Body')
        self.instance = ComponentInstance.objects.create(type=self.type, name='Base site body')

    def test_retrieve_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK, self.client.get(reverse('component-type-single', args=(self.type.id,)),
                                                             format='json').status_code)

    def test_retrieve_response(self):
        self.assertEqual(str(self.type.id), self.client.get(reverse('component-type-single', args=(self.type.id,)),
                                                            format='json').data['id'])

    def test_list_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK, self.client.get(reverse('component-type-list'), format='json').status_code)

    def test_list_response(self):
        self.assertEqual(str(self.type.id),
                         self.client.get(reverse('component-type-list'), format='json').data[0]['id'])
