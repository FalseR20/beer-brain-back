from rest_framework import permissions

from beer_brain.events import models


class EventEditOnlyHost(permissions.BasePermission):
    message = "You are not host of this event"

    def has_object_permission(self, request, view, obj: models.Event):
        if request.method in permissions.SAFE_METHODS:
            return obj.users.filter(id=request.user.id).exists()
        return obj.host == request.user


class TransactionEditMemberOrHost(permissions.BasePermission):
    message = "You are not member of this transaction or a host"

    def has_object_permission(self, request, view, obj: models.Transaction):
        if request.method in permissions.SAFE_METHODS:
            return True
        allowed_users = {
            *(movement.user for movement in obj.movements.all() if movement.delta != 0),
            obj.event.host,
        }
        return request.user in allowed_users


class MovementEditUserOrHost(permissions.BasePermission):
    message = "This movement isn't yours and you aren't a host"

    def has_object_permission(self, request, view, obj: models.Movement):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in {obj.user, obj.transaction.event.host}
