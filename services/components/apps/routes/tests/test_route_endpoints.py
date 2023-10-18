from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lib.authentication.utils import create_service_jwt, get_current_service_permissions
from ..models import Route, Site
from ...components.models import ComponentInstance, ComponentType


class RouteTest(APITestCase):

    def authenticate_by_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + create_service_jwt())

    def setUp(self):
        assert 'components:Route:GET' in get_current_service_permissions()
        self.authenticate_by_jwt()
        self.type = ComponentType.objects.create(react_name='Body', name='Body')
        self.component = ComponentInstance.objects.create(type=self.type, name='Base site body')
        self.site_with_routes_domain = 'subdomain.domain.tld'
        self.site = Site.objects.create(domain=self.site_with_routes_domain)
        self.site_without_routes_domain = 'subdomain.anotherdomain.tld'
        self.site_without_routes = Site.objects.create(domain=self.site_without_routes_domain)
        self.route = Route.objects.create(route='/page/<slug>/', site=self.site, component=self.component)
        self.route_homepage = Route.objects.create(route='/', site=self.site, component=self.component)
        self.route_complicated = Route.objects.create(route='/page/<slug>/skeleton/<slug>', site=self.site,
                                                      component=self.component)

    def test_retrieve_by_uuid_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(reverse('route-uuid-single', args=(self.route.id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_response(self):
        self.assertEqual(str(self.route.id),
                         self.client.get(reverse('route-uuid-single', args=(self.route.id,)), format='json').data['id'])

    def test_retrieve_by_domain_and_path_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(
                             reverse('route-path-single', args=(self.site_with_routes_domain, '/page/path/')),
                             format='json').status_code)

    def test_retrieve_by_domain_and_path_returns_404_for_non_existent_site(self):
        self.assertEqual(status.HTTP_404_NOT_FOUND,
                         self.client.get(reverse('route-path-single', args=('nonexistent.tld', '/page/test')),
                                         format='json').status_code)

    def test_retrieve_by_domain_and_path_returns_404_for_site_without_routes(self):
        self.assertEqual(status.HTTP_404_NOT_FOUND,
                         self.client.get(reverse('route-path-single', args=(self.site_without_routes, '/page/test')),
                                         format='json').status_code)

    def test_retrieve_by_domain_and_path_response(self):
        self.assertEqual(str(self.route.id),
                         self.client.get(reverse('route-path-single', args=(self.site.domain, '/page/test')),
                                         format='json').data['id'])

    def test_retrieve_by_domain_and_path_response_with_complicated_route(self):
        self.assertEqual(str(self.route_complicated.id),
                         self.client.get(
                             reverse('route-path-single', args=(self.site.domain, '/page/test/skeleton/test')),
                             format='json').data['id'])

    def test_retrieve_by_domain_and_path_response_for_homepage(self):
        self.assertEqual(str(self.route_homepage.id),
                         self.client.get(reverse('route-path-homepage', args=(self.site.domain,)), format='json').data[
                             'id'])
