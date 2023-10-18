from uuid import uuid4

from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .authorization import IsOwner, IsLoggedInOwner, is_loggedin, is_registered
from .models import User, ElevatedToken, IdentityToken
from .serializers import AuthenticatedUserSerializer, AuthorizedUserSerializer, AcceptPrivacyPolicySerializer, \
    CollectEmailSerializer, RegisterUserSerializer, LoginUserSerializer, CreateUserSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        if 'serializer_class' in kwargs:
            serializer_class = kwargs.pop('serializer_class')
        else:
            serializer_class = AuthorizedUserSerializer if is_loggedin(self.request) else AuthenticatedUserSerializer
        return serializer_class(*args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'retrieve':
            return [IsOwner()]
        if self.action == 'update':
            return [IsOwner()]
        if self.action == 'destroy':
            return [IsLoggedInOwner()]
        raise PermissionDenied('Unsupported action!')

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        # login user if possible
        if all([
            request.data.get('password', False),
            request.data.get('email', False)
        ]):
            user = None
            if user is None and request.data.get('email', False):
                try:
                    user = User.objects.get(email=request.data.get('email'))
                except User.DoesNotExist:
                    raise PermissionDenied('Email not found!')
                except User.MultipleObjectsReturned:
                    raise PermissionDenied('Multiple emails found!')
            if not user.is_registered:
                raise PermissionDenied('Not registered!')
            if not user.check_password(request.data.get('password')):
                raise PermissionDenied('Invalid password!')
            serializer = self.get_serializer(user, data={}, partial=True, serializer_class=LoginUserSerializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # create new user otherwise
        return Response(self.get_serializer(User.objects.create(username='user_{}'.format(uuid4())),
                                            serializer_class=CreateUserSerializer).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # register if possible
        if all([
            not is_registered(request),
            request.data.get('email', False),
            request.data.get('password', False),
            request.data.get('accepted_privacy_policy', False),
            request.data.get('accepted_terms_of_service', False),
        ]):
            serializer = self.get_serializer(instance, data=request.data, partial=True,
                                             serializer_class=RegisterUserSerializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # allow privacy policy update without login if not registered and privacy policy is not accepted
        if all([
            not is_registered(request),
            not instance.accepted_privacy_policy,
            request.data.get('accepted_privacy_policy', False)
        ]):
            serializer = self.get_serializer(instance,
                                             data={'accepted_privacy_policy': True},
                                             partial=True,
                                             serializer_class=AcceptPrivacyPolicySerializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # allow email update without login if not registered but accepted privacy policy
        if all([
            not is_registered(request),
            request.data.get('email', False),
            instance.accepted_privacy_policy
        ]):
            serializer = self.get_serializer(instance,
                                             data={'email': request.data.get('email')},
                                             partial=True,
                                             serializer_class=CollectEmailSerializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # allow update if logged in
        if is_loggedin(self.request):
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # deny in all other cases
        raise PermissionDenied('Not recognized request or not logged in.')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # log out
        if is_loggedin(self.request):
            token = ElevatedToken.objects.get(user=instance)
            token.delete()
            serializer = self.get_serializer(instance, data={}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise PermissionDenied('Cannot logout user that is not logged in.')


class UserByTokenView(UserView):
    lookup_field = None
    lookup_url_kwarg = 'token'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        try:
            user = ElevatedToken.objects.select_related('user').get(key=self.kwargs[lookup_url_kwarg]).user
        except ElevatedToken.DoesNotExist:
            try:
                user = IdentityToken.objects.select_related('user').get(key=self.kwargs[lookup_url_kwarg]).user
            except IdentityToken.DoesNotExist:
                raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
        self.check_object_permissions(self.request, user)
        return user
