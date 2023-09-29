from django.contrib.auth.models import User as AuthUser
from django.db import models


class User(models.Model):
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


class Event(models.Model):
    date = models.DateField(auto_now=True)
    description = models.CharField(max_length=256)
    is_closed = models.BooleanField()


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Deposit(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=256)


class Repayment(models.Model):
    payer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payer_member_id")
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="recipient_member_id")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
