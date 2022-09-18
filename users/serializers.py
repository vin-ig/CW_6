from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
	id = serializers.IntegerField(read_only=True)

	class Meta:
		model = User
		# exclude = ['password']
		fields = '__all__'

	# def is_valid(self, raise_exception=False):
	# 	self._location = self.initial_data.pop('location', None)
	# 	return super().is_valid(raise_exception=raise_exception)

	def create(self, validated_data):
		user = User.objects.create(**validated_data)
		user.set_password(user.password)
		# if self._location:
		# 	location_obj = Location.objects.get_or_create(name=self._location)[0]
		# 	user.location = location_obj
		user.save()
		return user


class CurrentUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ['password']


# from datetime import date
#
# from rest_framework import serializers
# from user.models import User, Location
#
#
# class UserAgeValidator:
# 	def __init__(self, min_age):
# 		self.min_age = min_age
#
# 	def __call__(self, born):
# 		today = date.today()
# 		age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
# 		if age < self.min_age:
# 			raise serializers.ValidationError(f'Users under {self.min_age} cannot register')
#
#
# class LocationSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Location
# 		fields = '__all__'
#
#
# class UserSerializer(serializers.ModelSerializer):
# 	location = serializers.SlugRelatedField(
# 		read_only=True,
# 		slug_field='name'
# 	)
#
# 	class Meta:
# 		model = User
# 		exclude = ['password']
#
#
# class UserCreateSerializer(serializers.ModelSerializer):
# 	id = serializers.IntegerField(read_only=True)
# 	location = serializers.SlugRelatedField(
# 		required=False,
# 		slug_field='name',
# 		queryset=Location.objects.all(),
# 	)
# 	birth_date = serializers.DateField(validators=[UserAgeValidator(9)])
#
# 	class Meta:
# 		model = User
# 		# exclude = ['password']
# 		fields = '__all__'
#
# 	def is_valid(self, raise_exception=False):
# 		self._location = self.initial_data.pop('location', None)
# 		return super().is_valid(raise_exception=raise_exception)
#
# 	def create(self, validated_data):
# 		user = User.objects.create(**validated_data)
# 		user.set_password(user.password)
# 		if self._location:
# 			location_obj = Location.objects.get_or_create(name=self._location)[0]
# 			user.location = location_obj
# 		user.save()
# 		return user
#
#
# class UserUpdateSerializer(serializers.ModelSerializer):
# 	id = serializers.IntegerField(read_only=True)
# 	location = serializers.SlugRelatedField(
# 		required=False,
# 		slug_field='name',
# 		queryset=Location.objects.all(),
# 	)
#
# 	class Meta:
# 		model = User
# 		# exclude = ['password']
# 		fields = '__all__'
#
# 	def is_valid(self, raise_exception=False):
# 		self._location = self.initial_data.pop('location', None)
# 		return super().is_valid(raise_exception=raise_exception)
#
# 	def save(self):
# 		user = super().save()
# 		user.set_password(user.password)
# 		if self._location:
# 			location_obj = Location.objects.get_or_create(name=self._location)[0]
# 			user.location = location_obj
# 		user.save()
# 		return user
#
#
# class UserDestroySerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ['id']
