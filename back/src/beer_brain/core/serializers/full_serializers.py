from rest_framework import serializers

from beer_brain.core import models
from beer_brain.core.serializers.profile_serializers import UserSerializer


class FullDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "member", "value", "description"]


class FullMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    deposits = FullDepositSerializer(many=True, read_only=True)

    class Meta:
        model = models.Member
        fields = ["id", "user", "deposits"]


class FullRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "value"]


class FullEventSerializer(serializers.ModelSerializer):
    members = FullMemberSerializer(many=True, read_only=True)
    repayments = FullRepaymentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Event
        fields = ["id", "date", "description", "is_closed", "members", "repayments"]
