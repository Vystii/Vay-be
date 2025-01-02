from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.utils import timezone
from v_utilities.views import LoginBaseViews, TemplateBaseViews
from v_utilities.models import SiteConfiguration
from v_utilities.services import VUtilitiesService
from users.models import Users
from django.utils.translation import gettext_lazy as _
import json
from .models import Course, CourseFile
from django.urls import reverse
from django.views.generic import DetailView
from django.forms import modelformset_factory
from .forms import CourseForm, CourseFileForm

class CoursesPage(TemplateBaseViews):
    class meta:
        abstract = False
    
    template_name = "v_utilities/dashboard-table.html"
    def get_context_data(self, **kwargs):
        courses = list()
        user_matricule = self.request.user.username
        year = VUtilitiesService.getCurrentYear()
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
    def getCourses(user_matricule:str, year:int = VUtilitiesService.getCurrentYear()):
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
    def get(self, request:HttpRequest, study_field:str, study_level:str, year:int=VUtilitiesService.getCurrentYear()):
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
            course  =  get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        else:
            year = self.kwargs.get('year')
            if year is None:
                year = VUtilitiesService.getCurrentYear()
            code_ue = self.kwargs.get('code_ue')
            course = get_object_or_404(Course, year=year, code_ue=code_ue)
        return course.toDict()
    

class CourseCreateView(View):
    template_name = 'v_utilities/form-base.html'

    def get(self, request):
        form = CourseForm()
        CourseFileFormSet = modelformset_factory(CourseFile, form=CourseFileForm, extra=1)
        formset = CourseFileFormSet(queryset=CourseFile.objects.none())
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request):
        form = CourseForm(request.POST, request.FILES)
        CourseFileFormSet = modelformset_factory(CourseFile, form=CourseFileForm, extra=1)
        formset = CourseFileFormSet(request.POST, request.FILES, queryset=CourseFile.objects.none())

        if form.is_valid() and formset.is_valid():
            
            course = form.save()
            # formset.
            courseFiles = formset.save(commit=False)
            for courseFile in courseFiles:
                courseFile.course = course
                courseFile.save()
            return redirect('user_course_page')  # Change this to the name of your course list view
        else:
            # print(f"******************\nerror_message: {formset.error_messages}\n***************************")
            # add message
            pass
        return render(request, self.template_name, {'form': form, 'formset': formset})