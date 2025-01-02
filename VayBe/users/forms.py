from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SchoolRequestFile, Users, SchoolRequest
from django_ckeditor_5.widgets import CKEditor5Widget

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ('first_name', 'last_name', 'email', 'study_field', 'study_level', 'is_staff')

class SchoolRequestForm(forms.ModelForm):
    class Meta:
        model = SchoolRequest
        fields = ['body']
        widgets = {
            "body" : CKEditor5Widget( attrs={"class": "django_ckeditor_5"}, config_name="default")
        }

class SchoolRequestFileForm(forms.ModelForm):
    class Meta:
        model = SchoolRequestFile
        fields = ['file']