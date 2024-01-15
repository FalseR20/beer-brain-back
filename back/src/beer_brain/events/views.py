from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, serializers, permissions


class EventListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects
    serializer_class = serializers.GetUpdateEventSerializer

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(users=self.request.user)


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


class EventRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.EventEditOnlyHost]
    queryset = models.Event.objects.all()
    serializer_class = serializers.GetUpdateEventSerializer


class FullEventRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.DetailedEventSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_event_api_view(request, *args, **kwargs):
    event: models.Event = get_object_or_404(models.Event, **kwargs)
    event.users.add(request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def leave_event_api_view(request, *args, **kwargs):
    event: models.Event = get_object_or_404(models.Event, **kwargs)
    if request.user == event.host:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"detail": "You cannot leave this event while you are a host"},
        )
    event.users.remove(request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)


class DepositCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Deposit
    serializer_class = serializers.CreateDepositSerializer

    def perform_create(self, serializer):
        event: models.Event = get_object_or_404(models.Event, pk=self.kwargs["event_id"])
        serializer.save(user=self.request.user, event=event)


class DepositRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.DepositEditOnlyUser]
    queryset = models.Deposit.objects
    serializer_class = serializers.GetDepositSerializer


class DepositListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Deposit.objects
    serializer_class = serializers.GetDepositSerializer


class RepaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Repayment
    serializer_class = serializers.CreateRepaymentSerializer

    def perform_create(self, serializer):
        event: models.Event = get_object_or_404(models.Event, pk=self.kwargs["event_id"])
        serializer.save(payer=self.request.user, event=event)


class RepaymentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.RepaymentEditOnlyPayerOrRecipient]
    queryset = models.Repayment.objects.all()
    serializer_class = serializers.GetRepaymentSerializer


class RepaymentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Repayment.objects.all()
    serializer_class = serializers.GetRepaymentSerializer
