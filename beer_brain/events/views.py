from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beer_brain.notifications.utils import notify_user, notify_users

from . import models
from . import notification_templates as nt
from . import paginators, permissions, serializers

User = get_user_model()


class EventListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EventSerializer
    pagination_class = paginators.EventsPaginator

    def get_queryset(self):
        return self.request.user.events.all()


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

    def perform_update(self, serializer: serializers.ChangeHostSerializer):
        event: models.Event = serializer.save()
        notify_users(
            users=event.users.exclude(id=event.host.id),
            message=nt.EVENT_CHANGED.format(event.host.id, event.id),
        )

    def perform_destroy(self, instance: models.Event):
        notify_users(
            users=instance.users.exclude(id=self.request.user.id),
            message=nt.EVENT_DELETED.format(self.request.user.id, instance.id),
        )
        instance.delete()


class ChangeHostAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, permissions.EventEditOnlyHost]
    queryset = models.Event.objects.all()
    serializer_class = serializers.ChangeHostSerializer
    http_method_names = ["patch"]

    def perform_update(self, serializer: serializers.ChangeHostSerializer):
        event: models.Event = serializer.save()
        notify_users(
            users=event.users.exclude(id=event.host.id),
            message=nt.HOST_CHANGED.format(event.host.id, event.id),
        )


@extend_schema(
    request=None,
    responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_event_api_view(request, *args, **kwargs):
    event: models.Event = get_object_or_404(models.Event, **kwargs)
    event.users.add(request.user)
    notify_users(
        users=event.users.exclude(id=request.user.id),
        message=nt.EVENT_JOINED.format(request.user.id, event.id),
    )
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

    # TODO: archive deposits
    deposits_to_delete = event.deposits.filter(user=request.user)
    for deposit in deposits_to_delete:
        notify_users(
            users=event.users.exclude(id=request.user.id),
            message=nt.DEPOSIT_DELETED.format(request.user.id, deposit.id, deposit.event.id),
        )
    deposits_to_delete.delete()

    # TODO: archive repayments
    repayments_to_delete = event.repayments.filter(
        Q(payer=request.user) | Q(recipient=request.user)
    )
    for repayment in repayments_to_delete:
        notify_users(
            users=event.users.exclude(id=request.user.id),
            message=nt.REPAYMENT_DELETED.format(request.user.id, repayment.id, repayment.event.id),
        )
    repayments_to_delete.delete()

    event.users.remove(request.user)
    notify_users(
        users=event.users.all(),
        message=nt.EVENT_LEFT.format(request.user.id, event.id),
    )
    return Response(status=status.HTTP_204_NO_CONTENT)


class DepositCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Deposit
    serializer_class = serializers.DepositSerializer

    def perform_create(self, serializer):
        event: models.Event = get_object_or_404(models.Event, pk=self.kwargs["event_id"])
        deposit: models.Deposit = serializer.save(user=self.request.user, event=event)
        notify_users(
            users=event.users.exclude(id=self.request.user.id),
            message=nt.DEPOSIT_CREATED.format(self.request.user.id, deposit.id, event.id),
        )


class DepositRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.DepositEditOnlyUserOrHost]
    queryset = models.Deposit.objects
    serializer_class = serializers.DepositSerializer

    def perform_update(self, serializer):
        deposit: models.Deposit = serializer.save()
        notify_users(
            users=deposit.event.users.exclude(id=self.request.user.id),
            message=nt.DEPOSIT_UPDATED.format(self.request.user.id, deposit.id, deposit.event.id),
        )

    def perform_destroy(self, instance: models.Deposit):
        notify_users(
            users=instance.event.users.exclude(id=self.request.user.id),
            message=nt.DEPOSIT_DELETED.format(
                self.request.user.id, instance.id, instance.event.id
            ),
        )
        instance.delete()


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
        repayment: models.Repayment = serializer.save(user=self.request.user, event=event)
        notify_user(
            user=repayment.recipient if self.request.user == repayment.payer else repayment.payer,
            message=nt.REPAYMENT_CREATED.format(
                self.request.user.id, repayment.id, repayment.event.id
            ),
        )


class RepaymentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.RepaymentEditOnlyPayerRecipientHost]
    queryset = models.Repayment.objects.all()
    serializer_class = serializers.RepaymentSerializer

    def perform_update(self, serializer):
        repayment: models.Repayment = serializer.save()
        notify_user(
            user=repayment.recipient if self.request.user == repayment.payer else repayment.payer,
            message=nt.REPAYMENT_UPDATED.format(
                self.request.user.id, repayment.id, repayment.event.id
            ),
        )

    def perform_destroy(self, instance: models.Repayment):
        notify_user(
            user=instance.recipient if self.request.user == instance.payer else instance.payer,
            message=nt.REPAYMENT_DELETED.format(
                self.request.user.id, instance.id, instance.event.id
            ),
        )
        instance.delete()


class RepaymentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Repayment.objects.all()
    serializer_class = serializers.RepaymentSerializer
