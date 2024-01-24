from django.contrib.auth import get_user_model
from rest_framework import serializers

from beer_brain.users.serializers import UserSerializer

from . import models

User = get_user_model()


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "user", "value", "description", "event"]
        extra_kwargs = {"event": {"read_only": True}}

    user = UserSerializer(read_only=True)


class CreateRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = [
            "id",
            "payer",
            "recipient",
            "recipient_username",
            "event",
            "value",
            "payed_at",
            "description",
        ]
        extra_kwargs = {
            "event": {"read_only": True},
            "payed_at": {"required": False},
        }

    payer = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    recipient_username = serializers.CharField(write_only=True)

    def create(self, validated_data: dict):
        recipient_username = validated_data.pop("recipient_username")
        recipient = User.objects.get(username=recipient_username)
        event: models.Event = validated_data["event"]
        if not event.users.filter(username=recipient_username).exists():
            raise serializers.ValidationError(
                {"recipient_username": "Recipient is not member of event"}
            )
        validated_data["recipient"] = recipient
        repayment = models.Repayment(**validated_data)
        repayment.save()
        return repayment


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "event", "value", "payed_at", "description"]
        extra_kwargs = {"event": {"read_only": True}}

    payer = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            "id",
            "name",
            "description",
            "date",
            "created_at",
            "is_closed",
            "users",
            "host",
            "deposits",
            "repayments",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "is_closed": {"required": False},
        }

    users = UserSerializer(many=True, read_only=True)
    host = UserSerializer(read_only=True)
    deposits = DepositSerializer(many=True, read_only=True)
    repayments = RepaymentSerializer(many=True, read_only=True)

    def create(self, validated_data: dict):
        event = models.Event(**validated_data)
        event.save()
        event.users.add(event.host)
        return event


class ChangeHostSerializer(EventSerializer):
    class Meta:
        model = models.Event
        fields = [
            "id",
            "name",
            "description",
            "date",
            "created_at",
            "is_closed",
            "users",
            "host",
            "new_host",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "description": {"read_only": True},
            "date": {"read_only": True},
            "created_at": {"read_only": True},
            "is_closed": {"read_only": True},
        }

    users = UserSerializer(many=True, read_only=True)
    host = UserSerializer(read_only=True)
    new_host = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        try:
            new_host = User.objects.get(username=validated_data["new_host"])
        except User.DoesNotExist as e:
            raise serializers.ValidationError({"new_host": "New host does not exist"}) from e
        if not new_host.events.filter(id=instance.id).exists():
            raise serializers.ValidationError({"new_host": "New host is not a member"})
        instance.host = new_host
        instance.save()
        return instance
