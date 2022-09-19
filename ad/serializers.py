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
	phone = serializers.SlugRelatedField(
		required=False,
		slug_field='phone',
		queryset=User.objects.all(),
	)
	author_first_name = serializers.SlugRelatedField(
		required=False,
		slug_field='first_name',
		queryset=User.objects.all(),
	)
	author_last_name = serializers.SlugRelatedField(
		required=False,
		slug_field='last_name',
		queryset=User.objects.all(),
	)
	author_id = serializers.SlugRelatedField(
		required=False,
		slug_field='id',
		queryset=User.objects.all(),
	)

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

	# def is_valid(self, raise_exception=False):
	# 	self._user = self.initial_data.pop('user', None)
	# 	print(self.get_initial())
	# 	return super().is_valid(raise_exception=raise_exception)

	# def create(self, validated_data):
	# 	ad = Ad.objects.create(**validated_data)
	# 	# if self._category:
	# 	# 	category_obj = Category.objects.get_or_create(name=self._category)[0]
	# 	# 	ad.category = category_obj
	# 	# 	ad.save()
	# 	ad.save()
	# 	return ad


class AdUpdateSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	# category = serializers.SlugRelatedField(
	# 	required=False,
	# 	slug_field='name',
	# 	queryset=Category.objects.all(),
	# )

	class Meta:
		model = Ad
		fields = '__all__'

	# def is_valid(self, raise_exception=False):
	# 	self._category = self.initial_data.pop('category', None)
	# 	return super().is_valid(raise_exception=raise_exception)

	def save(self):
		ad = super().save()
		# if self._category:
		# 	category_obj = Category.objects.get_or_create(name=self._category)[0]
		# 	ad.category = category_obj
		# 	ad.save()
		return ad


class AdDestroySerializer(serializers.ModelSerializer):
	class Meta:
		model = Ad
		fields = ['id']


# class SelectionListSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Selection
# 		fields = ['id', 'name']
#
#
# class SelectionDetailSerializer(serializers.ModelSerializer):
# 	owner = serializers.SlugRelatedField(
# 		read_only=True,
# 		slug_field='email'
# 	)
# 	items = AdSerializer(
# 		read_only=True,
# 		many=True
# 	)
#
# 	class Meta:
# 		model = Selection
# 		fields = '__all__'
#
#
# class SelectionCreateSerializer(serializers.ModelSerializer):
# 	id = serializers.IntegerField(read_only=True)
#
# 	class Meta:
# 		model = Selection
# 		fields = '__all__'
#
#
# class SelectionUpdateSerializer(serializers.ModelSerializer):
# 	id = serializers.IntegerField(read_only=True)
#
# 	class Meta:
# 		model = Selection
# 		fields = '__all__'
#
#
# class SelectionDestroySerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Selection
# 		fields = ['id']
