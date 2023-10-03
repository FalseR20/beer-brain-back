from rest_framework import serializers
from rest_framework.request import Request

from . import models


class CommonEventSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Event
        fields = "__all__"

    def get_members_count(self, event: models.Event) -> int:
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

    def get_initiator(self, event: models.Event) -> models.Member:
        request: Request = self.context["request"]
        user = models.User.objects.get(auth_user=request.user)
        member = models.Member()
        member.event = event
        member.user = user
        member.save()
        return member


# class MemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = 