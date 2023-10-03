from django.contrib.auth.models import User as AuthUser
from rest_framework import serializers

from ..core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ["username", "email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        auth_user = AuthUser(**validated_data)
        auth_user.set_password(password)
        auth_user.save()
        user = User()
        user.auth_user = auth_user
        user.save()
        return auth_user
