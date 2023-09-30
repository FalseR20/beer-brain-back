from rest_framework import serializers

from . import models


class CommonEventSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Event
        fields = "__all__"

    def get_members_count(self, event: models.Event) -> int:
        return models.Member.objects.filter(event=event).count()


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["description"]
