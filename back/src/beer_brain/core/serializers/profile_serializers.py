from django.contrib.auth.models import User
from rest_framework import serializers

from beer_brain.core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        profile = models.Profile()
        profile.auth_user = user
        profile.save()
        return user
