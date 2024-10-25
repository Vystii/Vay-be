from email.utils import unquote
from wsgiref.validate import validator
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _

# Create your models here.

class StudyLevel(models.Model):
    level_validator = validators.MinValueValidator(1)
    level = models.IntegerField(_("level"), unique=True, validators=[level_validator])
    code = models.CharField(_("code level"), max_length=5, primary_key=True)
    label = models.CharField(_("label"), max_length=20,blank=False)
    REQUIRED = ["niveau", "label"]
    
    constraints = [
            models.UniqueConstraint(fields=['level', 'code'], name='level_code_id'),
        ]
    
    def __str__(self):
        return self.label
    
class StudyField(models.Model):
    code_validator = validators.RegexValidator("^[A-Z]{3}")
    code = models.CharField(_("code"), max_length=3, primary_key=True, validators=[code_validator])
    label = models.CharField(_("Filiaire"), max_length=20)
    def __str__(self):
        return f"{self.code}-{self.label}"

class ModelBase(models.Model):

    studies_level = models.ForeignKey(StudyLevel, verbose_name=_("studies level"), on_delete=models.CASCADE, blank=False)
    study_field = models.ForeignKey(StudyField, verbose_name=_("study field"), on_delete=models.CASCADE, blank = False)
    class Meta:
        abstract = True
        