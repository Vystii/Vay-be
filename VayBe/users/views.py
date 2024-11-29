from django.http.response import HttpResponse as HttpResponse
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.views import LoginView
from v_utilities.views import LoginBaseViews
from course_manager.views import UserCourses
from django.contrib import messages
from .models import Users

class GetCourse(LoginBaseViews):    
    class meta:
        abstract = False
    def get(self, request:HttpRequest):
        user  = Users.objects.get(pk = request.user.id)            
        courses = UserCourses.getCourses(user_matricule = user.username)
        return JsonResponse(courses, safe=False)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
