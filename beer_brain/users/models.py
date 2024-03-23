from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .validators import UsernameValidator


class User(AbstractUser):
    username_validator = UsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=128,
        unique=True,
        help_text=_("Required. 3-128 characters. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = None
    full_name = models.CharField(_("full name"), max_length=128, blank=True)
    first_name = None
    last_name = None
    about = models.CharField(_("about field"), max_length=256, blank=True)
    # avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        constraints = [
            models.UniqueConstraint(Lower("username"), name="unique_lowercase_username")
        ]

    def get_full_name(self):
        return self.full_name
