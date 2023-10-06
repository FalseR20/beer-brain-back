from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.request import Request

from beer_brain.core import models
from beer_brain.core.serializers.all_fields_serializers import (
    MemberSerializer,
    DepositSerializer,
)


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


class CommonEventSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Event
        fields = "__all__"

    def retrieve(self):
        request: Request = self.context["request"]
        members = models.Member.objects.filter(user=request.user)
        return [member.event for member in members]

    @staticmethod
    def get_members_count(event: models.Event):
        return event.members.count()


class CreateEventSerializer(serializers.ModelSerializer):
    initiator = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Event
        fields = ["id", "date", "description", "is_closed", "initiator"]
        extra_kwargs = {
            "id": {"read_only": True},
            "date": {"read_only": True},
            "is_closed": {"read_only": True},
        }

    def get_initiator(self, event: models.Event):
        request: Request = self.context["request"]
        member = models.Member()
        member.event = event
        member.user = request.user
        member.save()
        return MemberSerializer(member).data


class FullMemberSerializer(serializers.ModelSerializer):
    deposits = DepositSerializer(many=True, read_only=True)

    class Meta:
        model = models.Member
        fields = ["id", "user", "event", "deposits"]


class GetFullEvent(serializers.ModelSerializer):
    members = FullMemberSerializer(many=True, read_only=True)

    class Meta:
        model = models.Event
        fields = ["id", "date", "description", "is_closed", "members"]
