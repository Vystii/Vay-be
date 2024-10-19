from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class MatriculeValidator(validators.RegexValidator):
    regex = r"^[1-9]{2}[A-Z]\d{3,4}$"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0