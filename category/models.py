from django.core.validators import MinLengthValidator
from django.db import models


class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=10, validators=[MinLengthValidator(5)], unique=True)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
		ordering = ['name']

	def __str__(self):
		return self.name
