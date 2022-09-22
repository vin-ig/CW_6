from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

from CW_6 import settings
from ad import views

ads_router = routers.SimpleRouter()
ads_router.register('ads', views.AdViewSet)

users_router = SimpleRouter()
users_router.register("api/api/users", UserViewSet, basename="users")

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/api/ads/', include('ad.urls')),

    path('', include(users_router.urls)),
    path('api/api/', include(ads_router.urls)),

	path('token/', TokenObtainPairView.as_view()),
	path('token/refresh/', TokenRefreshView.as_view()),

	path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
	path('api/schema/swagger-ui', SpectacularSwaggerView.as_view(url_name='schema')),
	path("api/redoc-tasks/", include("redoc.urls")),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
