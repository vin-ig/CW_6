from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE


def check_email_domain(email):
	address, domain = email.split('@')
	if domain == 'rambler.ru':
		raise ValidationError("Emails domain can`t be 'rambler.ru'")


class Location(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

	class Meta:
		verbose_name = 'Локация'
		verbose_name_plural = 'Локации'

	def __str__(self):
		return self.name


class User(AbstractUser):
	MEMBER = 'member'
	MODERATOR = 'moderator'
	ADMIN = 'admin'
	ROLES = [
		(MEMBER, 'Пользователь'),
		(MODERATOR, 'Модератор'),
		(ADMIN, 'Администратор'),
	]

	role = models.CharField(max_length=9, choices=ROLES)
	age = models.PositiveIntegerField(null=True, blank=True)
	location = models.ForeignKey(Location, on_delete=CASCADE, null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	email = models.EmailField(unique=True, validators=[check_email_domain])

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return self.username
