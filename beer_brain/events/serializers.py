from django.contrib.auth import get_user_model
from rest_framework import serializers

from beer_brain.users.serializers import UserSerializer

from . import models

User = get_user_model()


class SimpleMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movement
        fields = ["id", "user", "username", "delta", "cancel"]

    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)

    def create(self, validated_data):
        username = validated_data.pop("username")
        user = User.objects.get(username=username)
        return models.Movement.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        username = validated_data.pop("username", None)
        if username:
            user = User.objects.get(username=username)
            instance.username = user.username
        return super().update(instance, validated_data)


class SimpleTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ["id", "description", "datetime"]


class SimpleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            "id",
            "name",
            "description",
            "is_closed",
            "date",
            "created_at",
            "host",
            "users",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "is_closed": {"required": False},
        }

    users = UserSerializer(many=True, read_only=True)
    host = UserSerializer(read_only=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ["id", "description", "datetime", "movements"]

    movements = SimpleMovementSerializer(many=True, required=False)

    def validate(self, attrs):
        movements = attrs.get("movements", [])
        users = [movement["username"] for movement in movements]
        if len(users) != len(set(users)):
            raise serializers.ValidationError("There must be only one user")
        return attrs

    def create(self, validated_data: dict):
        movements_data = validated_data.pop("movements", [])
        transaction = models.Transaction.objects.create(**validated_data)
        movements = []
        for movement_data in movements_data:
            movement_serializer = SimpleMovementSerializer(data=movement_data)
            movement_serializer.is_valid(raise_exception=True)
            movement = movement_serializer.save(transaction=transaction)
            movements.append(movement)
            transaction.movements.add(*movements)
        transaction.save()
        return transaction

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


class DetailedTransactionSerializer(TransactionSerializer):
    class Meta:
        model = models.Transaction
        fields = ["id", "description", "datetime", "movements", "event"]

    event = SimpleEventSerializer(read_only=True)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            "id",
            "name",
            "description",
            "is_closed",
            "date",
            "created_at",
            "host",
            "users",
            "transactions",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "is_closed": {"required": False},
        }

    users = UserSerializer(many=True, read_only=True)
    host = UserSerializer(read_only=True)
    transactions = TransactionSerializer(many=True, read_only=True)

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
            "is_closed",
            "date",
            "created_at",
            "host",
            "users",
            "transactions",
            "new_host",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "description": {"read_only": True},
            "date": {"read_only": True},
            "created_at": {"read_only": True},
            "is_closed": {"read_only": True},
        }

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
