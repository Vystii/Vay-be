from django.contrib import admin

from v_utilities.models import StudyField, StudyLevel, SiteConfiguration

# Register your models here.
@admin.register(StudyLevel)
class StudyLevelAdmn(admin.ModelAdmin):
    pass

@admin.register(StudyField)
class StudyFieldAdmn(admin.ModelAdmin):
    pass

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    pass
