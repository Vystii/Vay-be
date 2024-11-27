from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest, JsonResponse
from v_utilities.views import LoginBaseViews
from course_manager.views import UserCourses
from .models import Users
from typing import Any


class GetCourse(LoginBaseViews):    
    class meta:
        abstract = False
    def get(self, request:HttpRequest):
        user  = Users.objects.get(pk = request.user.id)            
        courses = UserCourses.getCourses(user_matricule = user.username)
        return JsonResponse(courses, safe=False)
