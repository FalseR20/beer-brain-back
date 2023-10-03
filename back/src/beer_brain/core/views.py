from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import models, serializers
from .serializers import CreateUserSerializer


class RegistrationViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer


class EventsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        members: QuerySet[models.Member] = models.Member.objects.filter(
            user__auth_user=request.user
        )
        events = [member.event for member in members]
        serializer = serializers.CommonEventSerializer(events, many=True)
        return Response(serializer.data)


class CreateEventViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = models.Event
    serializer_class = serializers.CreateEventSerializer
