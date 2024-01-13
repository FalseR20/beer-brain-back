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


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="members", on_delete=models.CASCADE)


class Deposit(models.Model):
    member = models.ForeignKey(Member, related_name="deposits", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=256, blank=True)
    payed_at = models.DateTimeField(auto_now_add=True, blank=True)


class Repayment(models.Model):
    payer = models.ForeignKey(Member, related_name="repayments", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Member, related_name="receptions", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="repayments", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    payed_at = models.DateTimeField(auto_now_add=True, blank=True)
