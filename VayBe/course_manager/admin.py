from django.contrib import admin
from .models import Course
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"

admin.site.register(Course,CourseAdmin)