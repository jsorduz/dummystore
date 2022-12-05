from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from app_core.views import CustomTokenObtainPairView, CustomUserViewSet

router = DefaultRouter()
router.register("users", CustomUserViewSet, basename="user")

urlpatterns = [
    path(
        "jwt/create/",
        CustomTokenObtainPairView.as_view(),
        name="create-access-jwt-token",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="refresh-jwt-token"),
]
urlpatterns += router.urls
