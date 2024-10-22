from typing import Iterable
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

from v_utilities.validators import ModelValidator
from v_utilities.models import ModelBase

  
class Users(ModelBase, AbstractUser):
    class Meta:
        abstract = False
        
    username_validator = ModelValidator(regex = r"^[1-9]{2}[A-Z]\d{3,4}$")
    username = models.CharField(
        _("matricule"),
        max_length=7,
        unique=True,
        help_text=_(
            "Required. 6 or 7 characters or fewer."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that matricule already exists."),
        },
    )
    
    
    
    joinded_school= models.IntegerField(
        choices=[(r, r) for r in range(1980, timezone.now().year + 1)],
        default=timezone.now().year
    )
    
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if not self.username:
            # Get the last two digits of the year
            year_suffix = str(self.year)[-2:]
            # Generate the next unique letter and 4-digit combination
            next_unique = self.get_next_unique()
            # Combine to form the username
            self.username = f"{year_suffix}{next_unique}"
        print(f"force_insert: {force_insert}\nforce_update: {force_update}\nusing: {using}\nupdate_fieds: {update_fields}")
        return super().save()
    
    def get_next_unique(self):
        # Get the latest username
        latest = Users.objects.order_by('-id').first()
        if latest and latest.username:
            latest_code = latest.username[2:]  # Skip the year part
            # Convert the letter and digits to a number
            letter = latest_code[0]
            digits = latest_code[1:]
            number = (ord(letter) - ord('A')) * 10000 + int(digits)
            # Increment the number
            number += 1
            # Convert back to letter and digits
            new_letter = chr((number // 10000) + ord('A'))
            new_digits = str(number % 10000).zfill(4)
            return f"{new_letter}{new_digits}"
        else:
            # If no previous matricule, start with 'A0001'
            return "A0001"


    @property
    def year(self):
        return str(self.joinded_school)


    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "date_joined", "studies_level"]