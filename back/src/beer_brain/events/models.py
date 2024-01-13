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


class Deposit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="deposits", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=256, blank=True)
    payed_at = models.DateTimeField(auto_now_add=True, blank=True)


class Repayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer = models.ForeignKey(User, related_name="repayments", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="receptions", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="repayments", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    payed_at = models.DateTimeField(auto_now_add=True, blank=True)
