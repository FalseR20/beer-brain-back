from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, paginators, permissions, serializers

User = get_user_model()


@extend_schema(tags=["events"])
class EventListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects
    serializer_class = serializers.EventSerializer
    pagination_class = paginators.EventsPaginator

    def filter_queryset(self, queryset):
        return queryset.filter(users=self.request.user)


@extend_schema(tags=["events"])
class EventCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


@extend_schema(tags=["events"])
class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.EventEditOnlyHost]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


@extend_schema(tags=["events"])
class ChangeHostAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, permissions.EventEditOnlyHost]
    queryset = models.Event.objects.all()
    serializer_class = serializers.ChangeHostSerializer


@extend_schema(
    request=None,
    responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()},
    tags=["events"],
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
    tags=["events"],
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


@extend_schema(tags=["transactions"])
class TransactionCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Transaction
    serializer_class = serializers.TransactionSerializer

    def perform_create(self, serializer):
        event: models.Event = get_object_or_404(models.Event, pk=self.kwargs["event_id"])
        serializer.save(event=event)


@extend_schema(tags=["transactions"])
class TransactionRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.TransactionEditMemberOrHost]
    queryset = models.Transaction.objects
    serializer_class = serializers.TransactionSerializer


@extend_schema(tags=["transactions"])
class DetailedTransactionRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.TransactionEditMemberOrHost]
    queryset = models.Transaction.objects
    serializer_class = serializers.DetailedTransactionSerializer


@extend_schema(tags=["transactions"])
class TransactionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Transaction.objects
    serializer_class = serializers.TransactionSerializer


@extend_schema(tags=["movements"])
class MovementCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Movement
    serializer_class = serializers.SimpleMovementSerializer

    def perform_create(self, serializer):
        transaction: models.Transaction = get_object_or_404(
            models.Transaction, pk=self.kwargs["transaction_id"]
        )
        serializer.save(transaction=transaction)


@extend_schema(tags=["movements"])
class MovementRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.MovementEditUserOrHost]
    queryset = models.Movement.objects.all()
    serializer_class = serializers.SimpleMovementSerializer


@extend_schema(tags=["movements"])
class MovementListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Movement.objects.all()
    serializer_class = serializers.SimpleMovementSerializer
