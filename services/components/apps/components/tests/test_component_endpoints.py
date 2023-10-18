from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lib.authentication.utils import create_service_jwt, get_current_service_permissions

from ..models import ComponentInstance, ComponentType


class ComponentTest(APITestCase):

    def authenticate_by_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + create_service_jwt())

    def setUp(self):
        assert 'components:ComponentInstance:GET' in get_current_service_permissions()
        self.authenticate_by_jwt()
        self.type = ComponentType.objects.create(name='Body')
        self.instance = ComponentInstance.objects.create(type=self.type, name='Base site body')

    def test_retrieve_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK, self.client.get(reverse('component-single', args=(self.instance.id,)),
                                                             format='json').status_code)

    def test_retrieve_response(self):
        self.assertEqual(str(self.instance.id),
                         self.client.get(reverse('component-single', args=(self.instance.id,)), format='json').data[
                             'id'])

    def test_list_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK, self.client.get(reverse('component-list'), format='json').status_code)

    def test_list_response(self):
        self.assertEqual(str(self.instance.id), self.client.get(reverse('component-list'), format='json').data[0]['id'])
