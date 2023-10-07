from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from . import models, serializers


class UserViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class EventsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.MembersCountEventSerializer


class CreateEventViewSet(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class GetEventFull(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.FullEventSerializer
