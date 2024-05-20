from django.contrib.auth import get_user_model
from rest_framework import serializers

from beer_brain.users.serializers import UserSerializer

from . import models

User = get_user_model()


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "user", "value", "description", "event", "payed_at"]
        extra_kwargs = {
            "event": {"read_only": True},
            "payed_at": {"read_only": False, "required": False},
        }

    user = UserSerializer(read_only=True)


class CreateRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = [
            "id",
            "payer",
            "payer_id",
            "recipient",
            "recipient_id",
            "event",
            "value",
            "payed_at",
            "description",
        ]
        extra_kwargs = {
            "event": {"read_only": True},
            "payed_at": {"read_only": False, "required": False},
        }

    payer = UserSerializer(read_only=True)
    payer_id = serializers.IntegerField(write_only=True, required=False)
    recipient = UserSerializer(read_only=True)
    recipient_id = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data: dict):
        event: models.Event = validated_data["event"]
        user = validated_data.pop("user")
        recipient_id = validated_data.pop("recipient_id", None)
        payer_id = validated_data.pop("payer_id", None)
        if payer_id and recipient_id:
            msg = "You can set only payer or recipient"
            raise serializers.ValidationError(
                {
                    "recipient_username": msg,
                    "payer_username": msg,
                }
            )
        if not payer_id and not recipient_id:
            msg = "Recipient or payer is not set"
            raise serializers.ValidationError(
                {
                    "recipient_username": msg,
                    "payer_username": msg,
                }
            )

        if recipient_id:
            if recipient_id == user.id:
                raise serializers.ValidationError(
                    {"recipient_username": "Recipient and payer cannot be the same"}
                )
            recipient = User.objects.get(id=recipient_id)
            if not event.users.filter(id=recipient_id).exists():
                raise serializers.ValidationError(
                    {"recipient_username": "Recipient is not member of event"}
                )
            validated_data["recipient"] = recipient
            validated_data["payer"] = user
        else:
            if payer_id == user.id:
                raise serializers.ValidationError(
                    {"payer_username": "Payer and recipient cannot be the same"}
                )
            payer = User.objects.get(id=payer_id)
            if not event.users.filter(id=payer_id).exists():
                raise serializers.ValidationError(
                    {"payer_username": "Payer is not member of event"}
                )
            validated_data["payer"] = payer
            validated_data["recipient"] = user

        repayment = models.Repayment(**validated_data)
        repayment.save()
        return repayment


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = [
            "id",
            "payer",
            "recipient",
            "event",
            "value",
            "payed_at",
            "description",
        ]
        extra_kwargs = {
            "event": {"read_only": True},
            "payed_at": {"read_only": False, "required": False},
        }

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
            "host_id",
            "deposits",
            "repayments",
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
    host_id = serializers.IntegerField(write_only=True)

    def update(self, instance, validated_data):
        try:
            new_host = User.objects.get(id=validated_data["host_id"])
        except User.DoesNotExist as e:
            raise serializers.ValidationError({"host_id": "New host does not exist"}) from e
        if not new_host.events.filter(id=instance.id).exists():
            raise serializers.ValidationError({"host_id": "New host is not a member"})
        instance.host = new_host
        instance.save()
        return instance
