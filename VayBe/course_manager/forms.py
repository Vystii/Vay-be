from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models 

class AdminCourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ('code_ue', 'label', 'status','description', 'study_field', 'study_level',)

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ('label','description')

class CourseFileForm(forms.ModelForm):
    class Meta:
        model = models.CourseFile
        fields = ['file']


