from django.contrib.auth.models import User
from rest_framework import generics, views
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from . import models, serializers


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class EventListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.MembersCountEventSerializer


class EventCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class EventRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class FullEventRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.FullEventSerializer


class MemberAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request: Request, event_id: int):
        user = request.user
        event = get_object_or_404(models.Event, pk=event_id)
        if models.Member.objects.filter(user=user, event=event).exists():
            raise ValidationError({"detail": "You are already here"})
        member = models.Member.objects.create(user=user, event=event)
        return Response(serializers.MemberSerializer(member).data)
