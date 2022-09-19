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
	"""
	функция создания пользователя — в нее мы передаем обязательные поля
	"""

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
		"""
		функция для создания суперпользователя — с ее помощью мы создаем админинстратора
		это можно сделать с помощью команды createsuperuser
		"""

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

	role = models.CharField(max_length=9, choices=ROLES)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=12)
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	image = models.ImageField(upload_to='user_images/', blank=True, null=True)
	is_active = models.BooleanField(blank=True, null=True)

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


# def check_email_domain(email):
# 	address, domain = email.split('@')
# 	if domain == 'rambler.ru':
# 		raise ValidationError("Emails domain can`t be 'rambler.ru'")
#
#
# class Location(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	name = models.CharField(max_length=50)
# 	lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
# 	lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#
# 	class Meta:
# 		verbose_name = 'Локация'
# 		verbose_name_plural = 'Локации'
#
# 	def __str__(self):
# 		return self.name
#
#
# class User(AbstractUser):
# 	MEMBER = 'member'
# 	MODERATOR = 'moderator'
# 	ADMIN = 'admin'
# 	ROLES = [
# 		(MEMBER, 'Пользователь'),
# 		(MODERATOR, 'Модератор'),
# 		(ADMIN, 'Администратор'),
# 	]
#
# 	role = models.CharField(max_length=9, choices=ROLES)
# 	age = models.PositiveIntegerField(null=True, blank=True)
# 	location = models.ForeignKey(Location, on_delete=CASCADE, null=True, blank=True)
# 	birth_date = models.DateField(null=True, blank=True)
# 	email = models.EmailField(unique=True, validators=[check_email_domain])
#
# 	class Meta:
# 		verbose_name = 'Пользователь'
# 		verbose_name_plural = 'Пользователи'
#
# 	def __str__(self):
# 		return self.username
