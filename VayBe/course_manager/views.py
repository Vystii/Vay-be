from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import timezone
from v_utilities.views import LoginBaseViews, TemplateBaseViews
from users.models import Users
from django.utils.translation import gettext_lazy as _
import json
from .models import Course
from django.urls import reverse
from django.views.generic import DetailView


class CoursesPage(TemplateBaseViews):
    class meta:
        abstract = False
    
    template_name = "v_utilities/dashboard-table.html"
    def get_context_data(self, **kwargs):
        courses = list()
        user_matricule = self.request.user.username
        year = int(timezone.now().year)
        source_url = reverse("user_course", kwargs={"user_matricule":user_matricule}) 
        tableSettings ={
            "actions": [
                {"label":"action1","class": "url","token": "action1"},
                {"label":"action2","class": "url","token": "action2"},
            ],
            "table_header":[
                {"label": "Code","id": "code_ue"},
                {"label": "Titre","id": "label"},
                {"label": "Status","id": "status"},
                {"label": "Study field","id": "study_field"},
                {"label": "Study level","id": "study_level"}
            ]
        } 
        if user_matricule is not None:
            courses = UserCourses.getCourses(user_matricule, year=year)
        context = {
            "header": {"title": _("Your Courses")},
            "data_source": source_url,
            "tableSettings" : tableSettings,
            "jsonSettings" : json.dumps(tableSettings),
            'courses': courses
        }
        return context
    

# class UserCourses(LoginBaseViews):
# class UserCourses(View):
class UserCourses(LoginBaseViews):
    @staticmethod
    def getCourses(user_matricule:str, year:int = timezone.now().year):
        user = get_object_or_404(Users, username =user_matricule)
        std_field = user.study_field.code
        std_level = user.study_level.code
        if(user.has_perm("teach")):
            return Course.getCourses( year = year, teachers=user)
        return Course.getCourses(study_field_id=std_field, study_level_id = std_level, year = year)
        
    def post(self, request:HttpRequest, user_matricule:str, year:int=timezone.now().year):
        courses = list()
        if user_matricule is not None:
            courses = UserCourses.getCourses(user_matricule, year=year)
        return  JsonResponse(courses,safe=False)
    
    def get(self, request:HttpRequest, user_matricule:str, year:int=timezone.now().year):
        return self.post(request, user_matricule=user_matricule, year=year)

class ClassCourses(LoginBaseViews):
    class meta:
        abstract = False
    def get(self, request:HttpRequest, study_field:str, study_level:str, year:int=timezone.now().year):
        courses = Course.getCourses(study_field_id = study_field, study_level_id = study_level, year = year )
        return JsonResponse(courses, safe=False)

class Note(LoginBaseViews):
    class meta:
        abstract = False
    
    def get(self, request):
        return HttpResponse("notes")    
    

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_manager/course-details.html'
    context_object_name = 'course'
    
    def get_object(self):
        course = None
        if(self.kwargs.get('course_id')):
            print("*************************************************\n"+self.kwargs.get('course_id'))
            course  =  get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        else:
            year = self.kwargs.get('year')
            code_ue = self.kwargs.get('code_ue')
            course = get_object_or_404(Course, year=year, code_ue=code_ue)
        return course.toDict()