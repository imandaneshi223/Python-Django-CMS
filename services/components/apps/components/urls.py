from django.urls import path

from .views import ComponentView, TypeView

urlpatterns = [
    path('component_type/', TypeView.as_view({'get': 'list'}), name='component-type-list'),
    path('component_type/<uuid:pk>/', TypeView.as_view({'get': 'retrieve'}), name='component-type-single'),
    path('component/', ComponentView.as_view({'get': 'list'}), name='component-list'),
    path('component/<uuid:pk>/', ComponentView.as_view({'get': 'retrieve'}), name='component-single')
]
