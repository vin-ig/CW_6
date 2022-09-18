from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import CASCADE

from category.models import Category
from users.models import User


class Ad(models.Model):
	title = models.CharField(max_length=50, null=True)
	author = models.ForeignKey(User, on_delete=CASCADE)
	price = models.PositiveIntegerField()
	description = models.TextField(max_length=1000, null=True)
	created_at = models.DateTimeField(null=True)

	class Meta:
		verbose_name = 'Объявление'
		verbose_name_plural = 'Объявления'
		ordering = ['-created_at']

	def __str__(self):
		return self.title


class Comment(models.Model):
	text = models.CharField(max_length=1000)
	author = models.ForeignKey(User, on_delete=CASCADE)
	ad = models.ForeignKey(Ad, on_delete=CASCADE)
	created_at = models.DateTimeField()

	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы'

	def __str__(self):
		return self.text
