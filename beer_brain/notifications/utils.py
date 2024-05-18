from typing import Iterable

from . import models


def notify_users(users: Iterable[models.User], message: str) -> None:
    for user in users:
        notify_user(user, message)


def notify_user(user: models.User, message: str) -> None:
    models.Notification.objects.create(
        user=user,
        message=message,
    )
