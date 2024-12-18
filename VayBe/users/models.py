from ast import arg
from typing import Iterable
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field



from v_utilities.validators import ModelValidator
from v_utilities.models import ModelBase

  
class Users(ModelBase, AbstractUser):
    class Meta:
        permissions = [
            # Ths permission should be given be any way possible to the instructors
            ("handle_request", _("Can handle request")),
            ("teach", _("can teach a lesson"))
        ]
        abstract = False
    
    def __str__(self):
        self.is_superuser
        return f"{self.username}-{self.email}"
    
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
    
    is_staff = models.BooleanField(
        _("is teacher"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
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
    def is_request_handler(self):
        return self.has_perm("handle_request")
    
    @property
    def year(self):
        return str(self.joinded_school)

    def toDict(self):
        return {
            "username": self.username,
            "joinged_school": self.joinded_school,
            "is_staff": self.is_staff,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "date_joined", "studies_level"]
    
    

class PropertyModels(models.Model):
    
    owner = models.ForeignKey(Users, verbose_name=_("owner"), on_delete=models.CASCADE, blank = True, related_name="owned_%(class)s")
    
    class Meta:
        abstract = True


class SchoolRequest( PropertyModels):
    """_summary_

    Args:
        models (_type_): structure that represente request
    """
    receiver = models.ForeignKey(
        Users,
        verbose_name=_("receiver"),
        on_delete=models.CASCADE,
        # related_name="+",
        limit_choices_to=models.Q(user_permissions__codename="handle_request") | models.Q(is_superuser= True) | models.Q(is_staff=True),
        blank=False
    )
    processed = models.BooleanField(_("processed"), default= False)    
    body = CKEditor5Field(_("Body"), blank=True, null=True)
    class Meta:
        abstract = False
    
    REQUIRED_FIELDS = ["receiver", "sender", "body"]
    
    def toDict(self, keepDicts= False):
        url = reverse("request_page", args= [self.pk])
        return {
            "id": self.id,
            "receiver": self.receiver.toDict() if keepDicts else  f"{self.receiver.last_name} {self.receiver.first_name}",
            "sender": self.owner.toDict() if keepDicts else f"{self.owner.last_name} {self.owner.first_name}",
            "processed": self.processed,
            "body": self.body, 
            "url": url
        }