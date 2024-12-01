from django.http.response import HttpResponse as HttpResponse
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.views import LoginView
from v_utilities.views import LoginBaseViews, TemplateBaseViews
from course_manager.views import UserCourses
from django.contrib import messages
from .models import Users
from .dashboard_block.plugin_manager import PluginManager

class GetCourse(LoginBaseViews):    
    class meta:
        abstract = False
    def get(self, request:HttpRequest):
        user  = Users.objects.get(pk = request.user.id)            
        courses = UserCourses.getCourses(user_matricule = user.username)
        return JsonResponse(courses, safe=False)


class Dashboard(TemplateBaseViews):
    class meta:
        absract = False
        
    template_name = "users/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Dashboard'
        user:Users = self.request.user
        context['user'] = {
            "name": user.last_name,
            "surname": user.first_name,
            "matricule": user.username,
            "std_level": user.study_level,
            "std_field": user.study_field,
            "is_staff": user.is_staff
        }
        context['blocks'] = PluginManager.getBlocksInfos()
        return context

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
