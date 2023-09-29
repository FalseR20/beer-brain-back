from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models


class EventsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        members: QuerySet[models.Member] = models.Member.objects.filter(user=request.user)
        events = [member.event for member in members]

        content = {"message": "Hello, World!"}
        return Response(content)
