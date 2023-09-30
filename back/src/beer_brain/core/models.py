from django.contrib.auth.models import User as AuthUser
from django.db import models


class User(models.Model):
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)


class Event(models.Model):
    date = models.DateField(auto_now_add=True, null=False)
    description = models.CharField(max_length=256, null=False)
    is_closed = models.BooleanField(null=False, default=False)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)


class Deposit(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    description = models.CharField(max_length=256, null=False)


class Repayment(models.Model):
    payer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payer_member_id", null=False)
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="recipient_member_id", null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=False)
