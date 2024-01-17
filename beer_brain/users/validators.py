import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[A-Za-z_][a-zA-Z0-9_]{2,127}$"
    message = _(
        "Enter a valid username. "
        "This value may contain only ascii letters, numbers, and '_' character "
        "and don't start with a number have length 3-256"
    )
    flags = re.ASCII
