from django.contrib.auth import get_user_model
from rest_framework import serializers

from beer_brain.users.serializers import UserSerializer
from . import models

User = get_user_model()


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["id", "name", "description", "date", "created_at", "is_closed", "host", "users"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "is_closed": {"read_only": True},
        }

    host = UserSerializer(required=False)
    users = UserSerializer(many=True, read_only=True)

    def create(self, validated_data: dict):
        event = models.Event(**validated_data)
        event.save()
        event.users.add(validated_data["host"])
        return event


class GetUpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["id", "name", "description", "date", "created_at", "is_closed", "host", "users"]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "date": {"required": False},
            "created_at": {"read_only": True},
            "is_closed": {"required": False},
            "host": {"required": False},
        }

    host = UserSerializer(required=False)
    users = UserSerializer(many=True, read_only=True)

    def update(self, instance: models.Event, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.is_closed = validated_data.get("is_closed", instance.is_closed)
        instance.host = validated_data.get("host", instance.host)
        instance.save()
        return instance


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "user", "value", "description"]


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "event", "value"]


class DetailedDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "user", "value", "description"]

    user = UserSerializer(read_only=True)


class DetailedRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "value"]

    payer = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)


class DetailedEventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "full_name", "deposits", "repayments")

    deposits = DetailedDepositSerializer(many=True, read_only=True)
    repayments = DetailedRepaymentSerializer(many=True, read_only=True)


class DetailedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["id", "name", "description", "date", "is_closed", "users"]

    users = DetailedEventUserSerializer(many=True, read_only=True)
