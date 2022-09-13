import factory.django

from ad.models import Ad, Selection
from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	username = factory.Faker('name')
	password = 'password'
	role = 'admin'
	email = factory.Faker('email')
	birth_date = '1988-10-11'


class AdFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Ad

	name = 'test name 10 letters'
	price = 1300
	is_published = False
	author = factory.SubFactory(UserFactory)
