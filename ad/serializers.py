from datetime import datetime

from rest_framework import serializers

from ad.models import Ad, Comment
from users.models import User


class IsPublishedValidator:
	def __call__(self, value):
		if value:
			raise serializers.ValidationError("The value of the 'is_published' field cannot be True.")


class AdListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ad
		fields = ['pk', 'image', 'title', 'price', 'description']


class AdDetailSerializer(serializers.ModelSerializer):
	phone = serializers.CharField(source='author.phone')
	author_first_name = serializers.CharField(source='author.first_name')
	author_last_name = serializers.CharField(source='author.last_name')

	class Meta:
		model = Ad
		fields = [
			'pk',
			'image',
			'title',
			'price',
			'phone',
			'description',
			'author_first_name',
			'author_last_name',
			'author_id',
		]


class AdCreateSerializer(serializers.ModelSerializer):
	pk = serializers.IntegerField(read_only=True)
	price = serializers.IntegerField(required=True)
	phone = serializers.CharField(source='author.phone', required=False)
	author_first_name = serializers.CharField(source='author.first_name', required=False)
	author_last_name = serializers.CharField(source='author.last_name', required=False)

	class Meta:
		model = Ad
		fields = [
			'pk',
			'image',
			'title',
			'price',
			'description',
			'phone',
			'author_first_name',
			'author_last_name',
			'author_id',
		]

	def create(self, validated_data):
		ad = Ad.objects.create(**validated_data)
		ad.created_at = datetime.now()
		ad.save()

		return ad


class AdUpdateSerializer(serializers.ModelSerializer):
	pk = serializers.IntegerField(read_only=True)
	phone = serializers.CharField(source='author.phone')
	author_first_name = serializers.CharField(source='author.first_name')
	author_last_name = serializers.CharField(source='author.last_name')

	class Meta:
		model = Ad
		fields = [
			'pk',
			'image',
			'title',
			'price',
			'phone',
			'description',
			'author_first_name',
			'author_last_name',
			'author_id',
		]


class AdDestroySerializer(serializers.ModelSerializer):
	class Meta:
		model = Ad
		fields = ['id']


class CommentListSerializer(serializers.ModelSerializer):
	pk = serializers.IntegerField(read_only=True)
	# created_at = serializers.DateField(required=False)
	ad_id = serializers.CharField(source='ad.pk', required=False)
	author_id = serializers.CharField(source='author.pk', required=False)
	author_first_name = serializers.CharField(source='author.first_name', required=False)
	author_last_name = serializers.CharField(source='author.last_name', required=False)
	# author_image = serializers.CharField(source='author.author_image', required=False)

	class Meta:
		model = Comment
		fields = [
			'pk',
			'text',
			'created_at',
			'ad_id',
			'author_id',
			'author_first_name',
			'author_last_name',
			# 'author_image',
		]

	# def create(self, validated_data):
	# 	comment = Comment.objects.create(**validated_data)
	# 	comment.created_at = datetime.now()
	# 	comment.save()
	# 	return comment
