from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import models, serializers


class UserViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class EventsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        members: QuerySet[models.Member] = models.Member.objects.filter(
            user=request.user
        )
        events = [member.event for member in members]
        serializer = serializers.CommonEventSerializer(events, many=True)
        return Response(serializer.data)


class CreateEventViewSet(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = models.Event
    serializer_class = serializers.CreateEventSerializer


class GetEventFull(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Event.objects.all()
    serializer_class = serializers.GetFullEvent
