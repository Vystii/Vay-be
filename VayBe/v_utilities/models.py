from abc import abstractmethod
from email.utils import unquote
from pyclbr import Class
from wsgiref.validate import validator
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
# Create your models here.

class SiteConfiguration(models.Model):
    config_name = models.CharField(_("Config name"), primary_key=True, max_length=255)
    config_value = models.TextField(_("Value"), blank=True, null=True)
    # Add other settings fields as needed

    def __str__(self):
        return self.config_name

    class Meta:
        verbose_name = _("Site Configuration")
        verbose_name_plural = _("Site Configurations")

class StudyLevel(models.Model):
    level_validator = validators.MinValueValidator(1)
    level = models.IntegerField(_("level"), unique=True, validators=[level_validator])
    code = models.CharField(_("code level"), max_length=5, primary_key=True)
    label = models.CharField(_("label"), max_length=20,blank=False)
    REQUIRED = ["level", "label"]
    
    constraints = [
            models.UniqueConstraint(fields=['level', 'code'], name='level_code_id'),
        ]
    
    def __str__(self):
        return self.label
    
class StudyField(models.Model):
    code_validator = validators.RegexValidator("^[A-Z]{3}")
    code = models.CharField(_("code"), max_length=5, primary_key=True, validators=[code_validator])
    label = models.CharField(_("label"), max_length=20)
    def __str__(self):
        return f"{self.code}-{self.label}"
    
    def toDict(self):
        return {
            "code": self.code,
            "label": self.label
        }

class ModelBase(models.Model):
    study_level = models.ForeignKey(StudyLevel, verbose_name=_("studies level"), on_delete=models.CASCADE, blank=False)
    study_field = models.ForeignKey(StudyField, verbose_name=_("study field"), on_delete=models.CASCADE, blank = False)
    class Meta:
        abstract = True
        
    def toDict(self):
        return {
            "study_level": self.study_level,
            "study_field": self.study_field
        }
        
        
        
