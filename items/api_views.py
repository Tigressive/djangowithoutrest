from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from items.forms import ItemCreateForm
from items.serializers import ItemSerializer, BorrowSerializer, UserSerializer, UserItemSerializer
from items.models import Items


class ItemsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class UserItemList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Items.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('name', 'location')

    def get_queryset(self):
        return Items.objects.all().filter(owner=self.request.user)


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer

    def getByUsername(self, request, username):
        user = get_object_or_404(User, username)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    # def delete(self, request, *args, **kwargs):
    #     item_id = request.data.get('data')
    #     response = super().delete(request, *args, **kwargs)
    #     if response.status_code == 204:
    #         from django.core.cache import cache
    #         cache.delete('item_data_{}'.format(item_id))
    #     return response
    #
    # def update(self, request, *args, **kwargs):
    #     response = super().update(request, *args, **kwargs)
    #     if response.status_code == 200:
    #         from django.core.cache import cache
    #         item = response.data
    #         cache.set('item_data_{}'.format(item['id']), {
    #             'name': item['name'],
    #             'location': item['location'],
    #             'isPrivate': item['isPrivate'],
    #             'price': item['price'],
    #         })
    # return response


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('first_name', 'id')


class ItemList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Items.objects.all()
    serializer_class = UserItemSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('name', 'location')

    # pagination_class = ItemsPagination

    def get_queryset(self):
        isPrivate = self.request.query_params.get('isPrivate', None)
        queryset = Items.objects.all()
        if isPrivate is None:
            return queryset.filter(
                isPrivate=False
            )
        return queryset


class AuthTokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class AuthenticateView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)


class BorrowItem(RetrieveUpdateDestroyAPIView):
    queryset = Items.objects.all()
    serializer_class = BorrowSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            item = response.data

            cache.set('item_data_{}'.format(item['id']), {
                'name': item['name'],
                'location': item['location'],
                'isPrivate': item['isPrivate'],
                'price': item['price'],
            })
        return response


class ItemCreation(CreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            if name is not None and len(name) <= 2:
                raise ValidationError({'name': 'Must be more than 2 characters'})
        except ValueError:
            raise ValidationError({'name': 'A valid name is required'})
        return super().create(request, *args, **kwargs)


class ItemRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Items.objects.all()
    lookup_field = 'id'
    serializer_class = ItemSerializer

    def delete(self, request, *args, **kwargs):
        item_id = request.data.get('data')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('item_data_{}'.format(item_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            item = response.data
            cache.set('item_data_{}'.format(item['id']), {
                'name': item['name'],
                'location': item['location'],
                'isPrivate': item['isPrivate'],
                'price': item['price'],
            })
        return response
