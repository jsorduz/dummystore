from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from app_core.serializers import CustomTokenObtainPairSerializer, CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):  # pylint: disable=C0103
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
