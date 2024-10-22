from django.contrib import admin
from .models import Users, SchoolRequest
# Register your models here.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass
@admin.register(SchoolRequest)
class SchoolRequestAdmin(admin.ModelAdmin):
    pass