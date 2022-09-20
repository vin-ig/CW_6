from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import UpdateView
from rest_framework.permissions import IsAuthenticated

from ad.models import Ad, Comment
from ad.permissions import AdActionsPermission
from ad.serializers import AdListSerializer, AdCreateSerializer, AdUpdateSerializer, AdDestroySerializer, \
	AdDetailSerializer


# , SelectionListSerializer, \
# SelectionDetailSerializer, SelectionCreateSerializer, SelectionUpdateSerializer, SelectionDestroySerializer, \
# AdDestroySerializer


# from user.serializers import UserDestroySerializer


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(View):
	def get(self, request):
		return JsonResponse({'status': 'ok'}, status=200)


class AdListView(ListAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdListSerializer

	def get(self, request, *args, **kwargs):
		# Фильтр по категории
		cat_filter = request.GET.getlist('cat')
		if cat_filter:
			self.queryset = self.queryset.filter(category_id__in=cat_filter)

		# Поиск по тексту
		search_text = request.GET.get('text')
		if search_text:
			self.queryset = self.queryset.filter(name__icontains=search_text)

		# Поиск по городу
		location = request.GET.get('location')
		if location:
			self.queryset = self.queryset.filter(author__location__name__icontains=location)

		# Диапазон цен
		price_from, price_to = request.GET.get('price_from', ), request.GET.get('price_to')
		if price_from:
			self.queryset = self.queryset.filter(price__gte=price_from)
		if price_to:
			self.queryset = self.queryset.filter(price__lte=price_to)

		return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdDetailSerializer
# permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class AdUpdateView(UpdateAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdUpdateSerializer
	permission_classes = [IsAuthenticated]  # , AdActionsPermission]

	def perform_update(self, serializer):
		serializer.save(author=self.request.user)


class AdDeleteView(DestroyAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdDestroySerializer
# permission_classes = [IsAuthenticated, AdActionsPermission]


@api_view(["POST"])
@permission_classes([IsAuthenticated, AdActionsPermission])
def upload_image(request, pk):
	ad = Ad.objects.get(pk=pk)

	ad.image = request.FILES['image']
	ad.save()

	return JsonResponse({
		'id': ad.id,
		'name': ad.name,
		'author': ad.author.username,
		'price': ad.price,
		'description': ad.description,
		'image': ad.image.url if ad.image else None,
		'is_published': ad.is_published,
		'category': ad.category.name,
	}, safe=False)
