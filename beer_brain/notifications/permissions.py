from rest_framework import permissions

from . import models


class OnlyNotificationUser(permissions.BasePermission):
    message = "This notification isn't yours"

    def has_object_permission(self, request, view, obj: models.Notification):
        return obj.user == request.user
