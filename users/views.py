from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from users.models import User, Location
from users.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer, \
	LocationSerializer, CurrentUserSerializer


class UserListView(ListAPIView):
	queryset = User.objects.all()
	serializer_class = CurrentUserSerializer


class UserDetailView(RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = CurrentUserSerializer


class UserCreateView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserDestroySerializer
