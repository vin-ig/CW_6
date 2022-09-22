import datetime

from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import UpdateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ad.models import Ad, Comment
from ad.permissions import AdActionsPermission
from ad.serializers import AdListSerializer, AdCreateSerializer, AdUpdateSerializer, AdDestroySerializer, \
	AdDetailSerializer, CommentSerializer, AdSerializer


# @api_view(["POST"])
# @permission_classes([IsAuthenticated, AdActionsPermission])
# def upload_image(request, pk):
# 	ad = Ad.objects.get(pk=pk)
#
# 	ad.image = request.FILES['image']
# 	ad.save()
#
# 	return JsonResponse({
# 		'id': ad.id,
# 		'name': ad.name,
# 		'author': ad.author.username,
# 		'price': ad.price,
# 		'description': ad.description,
# 		'image': ad.image.url if ad.image else None,
# 		'is_published': ad.is_published,
# 		'category': ad.category.name,
# 	}, safe=False)


class AdViewSet(ModelViewSet):
	queryset = Ad.objects.all()
	serializer_class = AdSerializer
	serializer_action_classes = {
		'list': AdListSerializer,
		'retrieve': AdDetailSerializer,
		'create': AdCreateSerializer,
		'partial_update': AdUpdateSerializer,
		'destroy': AdDestroySerializer
	}

	def get_serializer_class(self):
		try:
			return self.serializer_action_classes[self.action]
		except (KeyError, AttributeError):
			return super().get_serializer_class()

	def perform_create(self, serializer):
		serializer.save(
			author=self.request.user,
			created_at=datetime.datetime.now(),
		)

	def perform_update(self, serializer):
		serializer.save(author=self.request.user)


class MyAdsView(ListAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdListSerializer

	def list(self, request, *args, **kwargs):
		user_id = self.request.user.id
		self.queryset = Ad.objects.filter(author=user_id)
		return super().list(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def get_queryset(self):
		return Comment.objects.filter(ad=self.kwargs['ad_pk'])

	def perform_create(self, serializer):
		serializer.save(
			author=self.request.user,
			created_at=datetime.datetime.now(),
			ad_id=self.kwargs['ad_pk']
		)

	def perform_update(self, serializer):
		serializer.save(
			author=self.request.user,
			ad_id=self.kwargs['ad_pk']
		)
