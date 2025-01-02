from django.contrib import admin
from django.forms import ModelForm
from .models import SchoolRequestFile, Users, SchoolRequest
from django_ckeditor_5.widgets import CKEditor5Widget

# Register your models here.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass

class SchoolRequestFileInline(admin.TabularInline):
    model = SchoolRequestFile
    extra = 1  # Number of empty forms to display
    fields = ['file']
    verbose_name = "SchoolRequest File"
    verbose_name_plural = "SchoolRequest Files"

class SchoolRequestAdmin(ModelForm):
    class Meta:
        model = SchoolRequest
        fields = '__all__'
        widgets = {
            'body': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="default"
              ),
        }

@admin.register(SchoolRequest)
class SchoolRequestFormAdmin(admin.ModelAdmin):
    form = SchoolRequestAdmin
    inlines = [SchoolRequestFileInline]
    empty_value_display = "-empty-"

@admin.register(SchoolRequestFile)
class CourseAdmin(admin.ModelAdmin):
    pass