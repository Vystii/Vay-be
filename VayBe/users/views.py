from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.utils import timezone
from django.http import HttpRequest, JsonResponse
from django.views import View
from course_manager.views import UserCourses
from .models import Users
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class GetCourse(View):    
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    def get(self, request:HttpRequest):
        user  = Users.objects.get(pk = request.user.id)            
        courses = UserCourses.getCourses(user_matricule = user.username)
        return JsonResponse(courses, safe=False)
