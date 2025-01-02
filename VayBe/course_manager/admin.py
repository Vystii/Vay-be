from django.contrib import admin
from .models import Course, CourseFile, Note
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import ModelForm

# Custom form for the Course model to use CKEditor widget
class CourseAdminForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="default"
              ),
        }

# Inline admin for CourseFile
class CourseFileInline(admin.TabularInline):
    model = CourseFile
    extra = 1  # Number of empty forms to display
    fields = ['file']
    verbose_name = "Course File"
    verbose_name_plural = "Course Files"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    inlines = [CourseFileInline]
    list_display = ["str_display", "id", "year", "code_ue"]
    empty_value_display = "-empty-"
    def str_display(self, obj):
        return str(obj)
    str_display.short_description = 'Verbose Name'

@admin.register(CourseFile)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass
