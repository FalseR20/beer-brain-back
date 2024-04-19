import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    is_closed = models.BooleanField(blank=True, default=False)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    host = models.ForeignKey(User, related_name="hosted_events", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="events")


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, related_name="transactions", on_delete=models.CASCADE)
    description = models.CharField(max_length=256, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)


class Movement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="movements", on_delete=models.CASCADE)
    transaction = models.ForeignKey(
        Transaction, related_name="movements", on_delete=models.CASCADE
    )
    delta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cancel = models.BooleanField(default=False)
