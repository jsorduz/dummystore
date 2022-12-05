from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app_core.models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        expires_in = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        data["token_type"] = settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0]
        data["expires_in"] = expires_in.total_seconds()

        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "password",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"password": {"write_only": True}}
