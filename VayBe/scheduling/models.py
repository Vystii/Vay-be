from django.utils.translation import gettext_lazy as _
from v_utilities.models import StudyField, StudyLevel
from django.core import validators
from django.db import models


class SchoolClass(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['study_level', 'study_field'], name='unique_class')
        ]
        
    def __str__(self)->str:
        return f"{self.study_level}_{self.study_field}"
    study_level = models.ForeignKey(StudyLevel, verbose_name=_("studies level"), on_delete=models.CASCADE, blank=False)
    study_field = models.ForeignKey(StudyField, verbose_name=_("study field"), on_delete=models.CASCADE, blank = False)
    expected_students  = models.IntegerField(_('Expected studends'), validators=[validators.MinValueValidator(1)])
    
    def buildId(self)->str:
        """
        Returns:
            str: le code the la filière + le code du niveau
        """
        return f"{self.study_field.code}_{self.study_level.code}"
