from django.contrib.auth import get_user_model
from rest_framework import serializers

from beer_brain.users.serializers import UserSerializer
from .. import models

User = get_user_model()


class FullDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "user", "value", "description"]

    user = UserSerializer(read_only=True)


class FullRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "value"]

    payer = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)


class FullEventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "full_name", "deposits", "repayments")

    deposits = FullDepositSerializer(many=True, read_only=True)
    repayments = FullRepaymentSerializer(many=True, read_only=True)


class FullEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["id", "name", "description", "date", "is_closed", "users"]

    users = FullEventUserSerializer(many=True, read_only=True)
