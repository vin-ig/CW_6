import enum
from datetime import date

from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE


class UserRoles(enum.Enum):
	ADMIN = 'admin'
	USER = 'user'


class UserManager(BaseUserManager):
	def create_user(self, email, first_name, last_name, phone, role, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
			phone=phone,
			role=role,
		)
		user.is_active = True
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, first_name, last_name, phone, role, password=None):
		user = self.create_user(
			email,
			first_name=first_name,
			last_name=last_name,
			phone=phone,
			password=password,
			role=role
		)

		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	ROLES = [
		(UserRoles.USER.value, 'Пользователь'),
		(UserRoles.ADMIN.value, 'Администратор'),
	]

	role = models.CharField(max_length=9, choices=ROLES, default=UserRoles.USER.value)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=12)
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	image = models.ImageField(upload_to='user_images/', blank=True, null=True)
	is_active = models.BooleanField(default=True, blank=True, null=True)

	@property
	def is_superuser(self):
		return self.is_admin

	@property
	def is_staff(self):
		return self.is_admin

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return self.is_admin

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]
	objects = UserManager()

	@property
	def is_admin(self):
		return self.role == UserRoles.ADMIN.value

	@property
	def is_user(self):
		return self.role == UserRoles.USER.value
