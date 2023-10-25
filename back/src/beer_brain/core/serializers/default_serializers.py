from rest_framework import serializers
from rest_framework.request import Request

from beer_brain.core import models


class EventSerializer(serializers.ModelSerializer):
    initiator = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Event
        fields = ["id", "date", "description", "is_closed", "initiator"]
        extra_kwargs = {
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
