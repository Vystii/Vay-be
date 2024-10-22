from atexit import register
from django.contrib import admin
from .models import Course, Note
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"

@admin.register(Note)
class NoteAdmn(admin.ModelAdmin):
    pass

# admin.site.regiscourseter(Course,CourseAdmin)