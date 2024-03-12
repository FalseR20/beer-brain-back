from rest_framework import permissions

from . import models


class EventEditOnlyHost(permissions.BasePermission):
    message = "You are not host of this event"

    def has_object_permission(self, request, view, obj: models.Event):
        if request.method in permissions.SAFE_METHODS:
            return obj.users.filter(id=request.user.id).exists()
        return obj.host == request.user


class DepositEditOnlyUserOrHost(permissions.BasePermission):
    message = "You are not creator of this deposit"

    def has_object_permission(self, request, view, obj: models.Deposit):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in (obj.user, obj.event.host)


class RepaymentEditOnlyPayerRecipientHost(permissions.BasePermission):
    message = "You are not payer or recipient of this repayment"

    def has_object_permission(self, request, view, obj: models.Repayment):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in (obj.payer, obj.recipient, obj.event.host)
