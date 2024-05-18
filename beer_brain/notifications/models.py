from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    is_read = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        self.is_read = True
        self.save()
