from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import models, serializers


class NotificationListView(generics.ListAPIView):
    serializer_class = serializers.NotificationSerializer
    queryset = models.Notification.objects
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_read"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class NotificationAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.NotificationMarkSerializer
    queryset = models.Notification.objects
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
