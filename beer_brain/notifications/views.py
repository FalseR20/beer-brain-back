from rest_framework import generics, status
from rest_framework.response import Response

from . import models, serializers


class NotificationListView(generics.ListAPIView):
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user)


class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user, is_read=False)


class MarkNotificationsView(generics.UpdateAPIView):
    http_method_names = ["patch"]

    def partial_update(self, request, *args, **kwargs):
        try:
            notification = models.Notification.objects.get(id=kwargs["pk"], user=request.user)
            notifications_to_mark_read = models.Notification.objects.filter(
                created_at__lte=notification.created_at, user=request.user, is_read=False
            )
            for n in notifications_to_mark_read:
                n.mark_as_read()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
