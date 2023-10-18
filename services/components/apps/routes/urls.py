from django.urls import path

from .views import SiteView, RouteView

urlpatterns = [
    path('site/', SiteView.as_view({'get': 'list'}), name='site-list'),
    path('site/<uuid:pk>/', SiteView.as_view({'get': 'retrieve'}), name='site-single'),
    path('route/', RouteView.as_view({'get': 'list'}), name='route-list'),
    path('route/<uuid:pk>/', RouteView.as_view({'get': 'retrieve'}), name='route-uuid-single'),
    path('route/<str:domain>/', RouteView.as_view({'get': 'retrieve'}), name='route-path-homepage'),
    path('route/<str:domain>/<path:path>/', RouteView.as_view({'get': 'retrieve'}), name='route-path-single'),
]
