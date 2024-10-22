from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from v_utilities.validators import ModelValidator
from v_utilities.models import ModelBase
from django.core import validators


class Course (ModelBase):
    # TODO: faire en sorte que le validateur intervenne également lorsqu'on essaye de créer un utilisateur
    # directement dans le code 

    codeUeValidator = validators.RegexValidator(regex=r"^[A-Z]{3}\d{3,4}$", message=_("The UE code must start with 3 letters followed by 3 or 4 numbers"))
    code_ue = models.CharField(
        _("code ue"),
        max_length=7,
        unique=True,
        primary_key=True,
        validators= [codeUeValidator],
        null=False
    )
    
    annee = models.IntegerField(
        _("year"),
        choices=[(r, r) for r in range(1980, timezone.now().year + 1)],
        default=timezone.now().year,
        null=False
    )
    
    intitule = models.CharField(_("course label"),max_length=7, default=None, blank=False)
    status = models.BooleanField(_("status"), default=True, null=False)
    
    REQUIRED_FIELDS = ["code_ue", "intitule"]