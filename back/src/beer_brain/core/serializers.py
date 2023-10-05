from rest_framework import serializers
from rest_framework.request import Request
from django.contrib.auth.models import User as AuthUser


from . import models


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
        user = models.User()
        user.auth_user = auth_user
        user.save()
        return auth_user


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = "__all__"


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = "__all__"


class CommonEventSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Event
        fields = "__all__"

    def get_members_count(self, event: models.Event):
        return models.Member.objects.filter(event=event).count()


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
        user = models.User.objects.get(auth_user=request.user)
        member = models.Member()
        member.event = event
        member.user = user
        member.save()
        return MemberSerializer(member).data


class GetFullEvent(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = "__all__"

    def get_members(self, event: models.Event):
        members = models.Member.objects.filter(event=event)
        return FullMemberSerializer(members, many=True).data


class FullMemberSerializer(serializers.ModelSerializer):
    deposits = serializers.SerializerMethodField()

    class Meta:
        model = models.Member
        fields = "__all__"

    def get_deposits(self, member: models.Member):
        deposits = models.Deposit.objects.filter(member=member)
        return DepositSerializer(deposits, many=True).data
