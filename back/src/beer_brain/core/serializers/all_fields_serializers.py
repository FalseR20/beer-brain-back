from rest_framework import serializers

from beer_brain.core import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["id", "date", "description", "is_closed"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ["id", "user", "event"]


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = ["id", "member", "value", "description"]


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repayment
        fields = ["id", "payer", "recipient", "event", "value"]
