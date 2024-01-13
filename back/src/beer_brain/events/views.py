from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


# class EventListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = models.Event.objects.all()
#     serializer_class = serializers.MembersCountEventSerializer
#
#     @staticmethod
#     def get(request: Request, **kwargs):
#         members = models.Member.objects.filter(user=request.user)
#         events = [member.event for member in members]
#         serializer = serializers.MembersCountEventSerializer(events, many=True)
#         return Response(serializer.data)


class EventCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.CreateEventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(host=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.GetUpdateEventSerializer

    def update(self, request, *args, **kwargs):
        event: models.Event = self.get_object()
        if request.user != event.host:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"detail": "You are not a host of this event"},
            )
        return super().update(request, *args, **kwargs)


class FullEventRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.DetailedEventSerializer
