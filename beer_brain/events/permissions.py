from rest_framework import permissions

from . import models


class EventEditOnlyHost(permissions.BasePermission):
    message = "You are not host of this event"

    def has_object_permission(self, request, view, obj: models.Event):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.host == request.user


class DepositEditOnlyUser(permissions.BasePermission):
    message = "You are not creator of this deposit"

    def has_object_permission(self, request, view, obj: models.Deposit):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class RepaymentEditOnlyPayerOrRecipient(permissions.BasePermission):
    message = "You are not payer or recipient of this repayment"

    def has_object_permission(self, request, view, obj: models.Repayment):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in (obj.payer, obj.recipient)
