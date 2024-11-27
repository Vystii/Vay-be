from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import timezone
from v_utilities.views import LoginBaseViews
from users.models import Users

from .models import Course
from course_manager.models import Course as ModelCourse

class UserCourses(LoginBaseViews):
    class meta:
        abstract = False
    
    @staticmethod
    def getCourses(user_matricule:str, year:int = timezone.now().year):
        user = get_object_or_404(Users, username =user_matricule)
        std_field = user.study_field.code
        std_level = user.study_level.code
        print(f"user_id: {user}")
        if(user.has_perm("teach")):
            return ModelCourse.getCourses(study_field_id=std_field, study_level_id = std_level, year = year, teachers=user)
        return ModelCourse.getCourses(study_field_id=std_field, study_level_id = std_level, year = year)
        
    def get(self, request:HttpRequest, user_matricule:str, year:int=timezone.now().year):
        courses = list()
        if user_matricule is not None:
            courses = UserCourses.getCourses(user_matricule, year=year)
        return  JsonResponse(courses,safe=False)


class ClassCourses(LoginBaseViews):
    class meta:
        abstract = False
    def get(self, request:HttpRequest, study_field:str, study_level:str, year:int=timezone.now().year):
        courses = ModelCourse.getCourses(study_field_id = study_field, study_level_id = study_level, year = year )
        return JsonResponse(courses, safe=False)
class Note(LoginBaseViews):
    class meta:
        abstract = False
    
    def get(self, request):
        return HttpResponse("notes")    
    
