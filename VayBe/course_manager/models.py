from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from v_utilities.validators import ModelValidator
from v_utilities.models import ModelBase
from django.core import validators
from users.models import Users
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
    
class Note(models.Model):
    def __str__(self):
        return f"{self.note}-{self.student.username}"
    
    student = models.ForeignKey(Users, verbose_name= _("student"), on_delete=models.CASCADE, related_name="+")
    course = models.ForeignKey(Course, verbose_name= _("course"), on_delete=models.CASCADE)
    correcteur = models.ForeignKey(Users, verbose_name= _("corrector"), on_delete=models.DO_NOTHING, related_name="+")
    note = models.IntegerField(_("note"))
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='custom_id'),
        ]