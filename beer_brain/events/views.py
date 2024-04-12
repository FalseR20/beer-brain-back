from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, paginators, permissions, serializers

User = get_user_model()


class EventListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects
    serializer_class = serializers.EventSerializer
    pagination_class = paginators.EventsPaginator

    def filter_queryset(self, queryset):
        return queryset.filter(users=self.request.user)


class EventCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.EventEditOnlyHost]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class ChangeHostAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, permissions.EventEditOnlyHost]
    queryset = models.Event.objects.all()
    serializer_class = serializers.ChangeHostSerializer


@extend_schema(
    request=None,
    responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_event_api_view(request, *args, **kwargs):
    event: models.Event = get_object_or_404(models.Event, **kwargs)
    event.users.add(request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    request=None,
    responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()},
)
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
    serializer_class = serializers.DepositSerializer

    def perform_create(self, serializer):
        event: models.Event = get_object_or_404(models.Event, pk=self.kwargs["event_id"])
        serializer.save(user=self.request.user, event=event)


class DepositRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.DepositEditOnlyUserOrHost]
    queryset = models.Deposit.objects
    serializer_class = serializers.DepositSerializer


class DepositListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Deposit.objects
    serializer_class = serializers.DepositSerializer


class RepaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Repayment
    serializer_class = serializers.CreateRepaymentSerializer

    def perform_create(self, serializer):
        event: models.Event = get_object_or_404(models.Event, pk=self.kwargs["event_id"])
        serializer.save(user=self.request.user, event=event)


class RepaymentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.RepaymentEditOnlyPayerRecipientHost]
    queryset = models.Repayment.objects.all()
    serializer_class = serializers.RepaymentSerializer


class RepaymentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Repayment.objects.all()
    serializer_class = serializers.RepaymentSerializer
