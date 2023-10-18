from django.urls import path, register_converter

from .views import UserView, UserByTokenView


class TokenConverter:
    regex = '[a-zA-Z0-9]{40}'

    @staticmethod
    def to_python(value):
        return str(value)

    @staticmethod
    def to_url(value):
        return str(value)


register_converter(TokenConverter, 'token')

urlpatterns = [
    path('user/', UserView.as_view({'post': 'create'}), name='users'),
    path('user/<uuid:pk>/',
         UserView.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
         name='user-single-by-uuid'),
    path('user/<token:token>/',
         UserByTokenView.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
         name='user-single-by-token')
]
