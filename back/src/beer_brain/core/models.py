from django.contrib.auth.models import User as AuthUser
from django.db import models


class User(models.Model):
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


class Debt(models.Model):
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now=True)
    creditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creditor_user_id")
    debtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="debtor_user_id")
