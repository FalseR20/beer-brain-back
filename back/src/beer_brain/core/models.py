from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Event(models.Model):
    date = models.DateField(auto_now_add=True, null=False)
    description = models.CharField(max_length=256, null=False)
    is_closed = models.BooleanField(null=False, default=False)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    event = models.ForeignKey(Event, related_name="members", on_delete=models.CASCADE, null=False)


class Deposit(models.Model):
    member = models.ForeignKey(Member, related_name="deposits", on_delete=models.CASCADE, null=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    description = models.CharField(max_length=256, null=False)


class Repayment(models.Model):
    payer = models.ForeignKey(Member, related_name="repayments", on_delete=models.CASCADE, null=False)
    recipient = models.ForeignKey(Member, related_name="receptions", on_delete=models.CASCADE, null=False)
    event = models.ForeignKey(Event, related_name="repayments", on_delete=models.CASCADE, null=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=False)
