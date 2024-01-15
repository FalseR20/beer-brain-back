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
        fields = [
            "id",
            "name",
            "description",
            "date",
            "created_at",
            "is_closed",
            "host",
            "users",
            "new_host",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "date": {"required": False},
            "created_at": {"read_only": True},
            "is_closed": {"required": False},
        }

    host = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    new_host = serializers.CharField(required=False)

    def update(self, instance: models.Event, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.is_closed = validated_data.get("is_closed", instance.is_closed)
        if new_host_username := validated_data.get("new_host"):
            try:
                new_host = User.objects.get(username=new_host_username)
            except User.DoesNotExist as e:
                raise serializers.ValidationError({"new_host": "New host does not exist"}) from e
            if not new_host.events.filter(id=instance.id).exists():
                raise serializers.ValidationError({"new_host": "New host is not a member"})
            instance.host = new_host
        instance.save()
        return instance


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


class DetailedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "full_name", "deposits", "repayments")

    deposits = DetailedDepositSerializer(many=True, read_only=True)
    repayments = DetailedRepaymentSerializer(many=True, read_only=True)


class DetailedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["id", "name", "description", "date", "is_closed", "users"]

    users = DetailedUserSerializer(many=True, read_only=True)


# create


class CreateDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "user", "value", "description", "event"]
        extra_kwargs = {"event": {"read_only": True}}

    user = UserSerializer(read_only=True)


class GetDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "user", "value", "description", "event"]
        extra_kwargs = {
            "value": {"required": False},
            "description": {"required": False},
            "event": {"read_only": True},
        }

    user = UserSerializer(read_only=True)


class CreateRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "recipient_username", "event", "value", "payed_at"]
        extra_kwargs = {"event": {"read_only": True}, "payed_at": {"required": False}}

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


class GetRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "event", "value", "payed_at"]
        extra_kwargs = {
            "event": {"read_only": True},
            "value": {"required": False},
            "payed_at": {"required": False},
        }

    payer = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
