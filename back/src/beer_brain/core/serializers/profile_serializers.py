from django.contrib.auth.models import User
from rest_framework import serializers

from beer_brain.core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        profile = models.Profile()
        profile.auth_user = user
        profile.save()
        return user


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class PublicProfileSerializer(serializers.ModelSerializer):
    auth_user = PublicUserSerializer()

    class Meta:
        model = models.Profile
        fields = ["auth_user"]


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class PrivateProfileSerializer(serializers.ModelSerializer):
    auth_user = PrivateUserSerializer()

    class Meta:
        model = models.Profile
        fields = ["auth_user"]
