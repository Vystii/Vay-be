from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from v_utilities.validators import ModelValidator
from v_utilities.models import ModelBase
from django.core import validators
from django.core.exceptions import ValidationError
from users.models import Users, PropertyModels
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise validators.ValidationError(_("Only PDF files are allowed."))

class Course(ModelBase):
    # Ensure the validator also works when creating a user directly in the code
    codeUeValidator = validators.RegexValidator(
        regex=r"^[A-Z]{3,4}\d{3,4}$",
        message=_("The UE code must start with 3 letters followed by 3 or 4 numbers")
    )
    code_ue = models.CharField(
        _("code ue"),
        max_length=8,
        validators=[codeUeValidator],
        null=False
    )

    year = models.IntegerField(
        _("year"),
        choices=[(r, r) for r in range(1980, timezone.now().year + 1)],
        default=timezone.now().year,
        null=False
    )

    label = models.CharField(_("course label"), max_length=50, default=None, blank=False)
    description = CKEditor5Field(_("description"), blank=True, null=True)
    status = models.BooleanField(_("status"), default=True, null=False)

    teachers = models.ManyToManyField(
        Users,
        verbose_name=_("teacher"),
        limit_choices_to=models.Q(
            user_permissions__name="teach"
        ) | models.Q(is_superuser=True),
        default=1,
    )

    REQUIRED_FIELDS = ["code_ue", "label"]

    class Meta:
        abstract = False
        constraints = [
            models.UniqueConstraint(fields=['code_ue', 'year'], name='unique_course')
        ]

    def get_absolute_url(self):
        return reverse('course_detail', args=[self.year, self.code_ue])

    def toDict(self):
        return {
            "id": self.id,
            "year": self.year,
            "status": self.status,
            "label": self.label,
            "code_ue": self.code_ue,
            "study_field": self.study_field.label,
            "study_level": self.study_level.label,
            "description": self.description,
            "teachers": [teacher.toDict() for teacher in self.teachers.all()],
            "files": [course_file.toDict() for course_file in self.coursefile_set.all()],
            "url": self.get_absolute_url()
        }

    @staticmethod
    def getCourses(**args):
        query_filter = {"status": True} | args
        params = {key: value for key, value in query_filter.items() if value is not None}
        courses = Course.objects.filter(**params)
        return [course.toDict() for course in courses]

class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(_("file"), upload_to='uploads/pdfs/', validators=[validate_pdf])

    def toDict(self):
        return {
            "file" : {
                "name": self.file.name.split("/")[-1],
                "url": self.file.url
            },
            "course": {
                "code": self.course.code_ue,
                "year": self.course.year
            }
        }
        
    def __str__(self):
        return f"File for {self.course.label}"


class NoteType(models.Model):
    label = models.CharField(_("Label"), max_length=50, default=None, blank=False)
    percentage = models.IntegerField(_("percentage"), validators=[validators.MinValueValidator(20), validators.MaxValueValidator(100)], blank=False, default=30)

    class Meta:
        verbose_name = _("Type de note")
        verbose_name_plural = _("types de notes")

    def clean(self):
        total_percentage = sum(note_type.percentage for note_type in NoteType.objects.filter(course=self.course)) + self.percentage
        if total_percentage > 100:
            raise ValidationError(_("The total percentage of note types for a course cannot exceed 100%. The current total would be %(total)s%%.") % {'total': total_percentage})

    def save(self, *args, **kwargs):
        self.clean()  # Call the custom validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label
    
class Note(PropertyModels):
    def __str__(self):
        return f"{self.note}-{self.student.username}"
    
    course = models.ForeignKey(Course, verbose_name=_("course"), on_delete=models.CASCADE)
    student = models.ForeignKey(Users, verbose_name=_("student"), on_delete=models.CASCADE, related_name="+")
    correcteur = models.ForeignKey(Users, verbose_name=_("corrector"), on_delete=models.DO_NOTHING, related_name="+")
    note_type = models.ForeignKey(NoteType, verbose_name=_("Note type"), on_delete=models.PROTECT, related_name="+", null=True)
    note = models.IntegerField(_("note"))

    class Meta:
            constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='custom_id'),
        ]
