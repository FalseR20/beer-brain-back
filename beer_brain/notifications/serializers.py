from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "message", "created_at", "is_read")


class NotificationMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "message", "created_at", "is_read")
        extra_kwargs = {
            "message": {"read_only": True},
            "created_at": {"read_only": True},
        }
