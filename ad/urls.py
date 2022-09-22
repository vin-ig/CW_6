from django.urls import path, include
from rest_framework import routers

from ad import views
from ad.views import CommentViewSet

router = routers.SimpleRouter()
router.register('comments', CommentViewSet)

urlpatterns = [
	path('', views.AdListView.as_view(), name='ad_list'),
	path('create/', views.AdCreateView.as_view(), name='ad_create'),
	path('<int:pk>/', views.AdDetailView.as_view(http_method_names=['get']), name='ad_detail'),
	path('<int:pk>/update/', views.AdUpdateView.as_view(), name='ad_update'),
	path('<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),

	path('me/', views.MyAdsView.as_view(), name='my_ads'),

	path('<int:ad_pk>/', include(router.urls), name='comments'),
	# path('<int:pk>/comments/', views.CommentListView.as_view(), name='comments_list'),
	# path('<int:pk>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),

	# path('<int:pk>/upload_image/', views.AdImageView.as_view(), name='ad_image'),
	path('<int:pk>/upload_image/', views.upload_image, name='ad_image'),
]
