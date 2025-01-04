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
from .models import Course, CourseFile, Note as NoteModel
from django.urls import reverse
from django.views.generic import DetailView
from django.forms import ValidationError, modelformset_factory
from .forms import CourseForm, CourseFileForm, AdminCourseForm


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

class GivingNotePages(CoursesPage):
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        return context
      
class UserCourses(LoginBaseViews):
    @staticmethod
    def getCourses(user_matricule:str, year:int = VUtilitiesService.getCurrentYear()):
        user = get_object_or_404(Users, username =user_matricule)
        std_field = user.study_field.code
        std_level = user.study_level.code
        if(user.has_perm("teach")):
            return Course.getCourses( year = year, teachers=user)
        return Course.getCourses(study_field_id=std_field, study_level_id = std_level, year = year, status = True)
        
    def post(self, request:HttpRequest, user_matricule:str, year:int=VUtilitiesService.getCurrentYear()):
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
    

class CourseDetailView(LoginBaseViews):
    template_name = "course_manager/course-details.html"
    context_object_name = 'course'


    def getDatas(self, kwargs):
        if "course_id" in kwargs:
            course_id = kwargs["course_id"]
            datas = self.get_context_data(course_id)
            datas["course" ] = datas["course_details"]
            return datas
        elif "code_ue" in kwargs:
            code_ue = kwargs["code_ue"]
            year = kwargs["year"] if "year" in kwargs else VUtilitiesService.getCurrentYear()
            course = get_object_or_404(Course, code_ue=code_ue, year=year)
            datas = self.get_context_data(course.id)
            datas["course" ] = datas["course_details"]
            return datas
        return None
    
    def get(self, request, *args, **kwargs):
        datas = self.getDatas(kwargs)
        if datas is None:
            return HttpResponse("404")
        if datas["can_edit"]:
            datas["actions"] = [
                {
                    "label":"Notes",
                    "url": reverse("submit_notes_page", kwargs={"course_id": datas["course_details"]["id"]})
                }
            ]
        return render(request, self.template_name, datas)
    
    def post(self, request, *args, **kwargs):
        course_id = None
        if "course_id" in kwargs:
            course_id = kwargs["course_id"]
        elif "code_ue" in kwargs:
            code_ue = kwargs["code_ue"]
            year = kwargs["year"] if "year" in kwargs else VUtilitiesService.getCurrentYear()
            course = get_object_or_404(Course, code_ue=code_ue, year=year)
            course_id = course.id
        else:
            return HttpResponse("404")
        course_instance = get_object_or_404(Course, id=course_id)
        form = CourseForm(request.POST, instance=course_instance)
        CourseFileFormSet = modelformset_factory(CourseFile, form=CourseFileForm, extra=10)
        
        formset = CourseFileFormSet(request.POST, request.FILES, queryset=CourseFile.objects.filter(course=course_instance))
        
        if form.is_valid() and formset.is_valid():
            form.save()
            filesForm = formset.save(commit=False)
            for fileForm in filesForm:
                if fileForm.file:
                    fileForm.course = course_instance
                    fileForm.save()
        else:
            datas = self.get_context_data(course_id)
            datas['formset']['fileForm'] = formset
                    
        datas['formset']['form'] = form
        return render(request, self.template_name, datas)

    def get_context_data(self, course_id):
        user = self.request.user
        course = get_object_or_404(Course, id=course_id)
        form = CourseForm(instance=course)
        CourseFileFormSet = modelformset_factory(CourseFile, form=CourseFileForm, extra=1)
        fileForm = CourseFileFormSet(queryset=CourseFile.objects.filter(course=course))
        return {
            "isTeacher": user.user_permissions.filter(codename='teach').exists() or user.is_superuser,
            "can_edit":  user in [teacher for teacher in course.teachers.all()],
            "modal_id": "form_edit_course",
            "course_details": course.toDict(),
            "formset": {"form": form, "fileForm": fileForm}
        }

    

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
            # add message
            pass
        return render(request, self.template_name, {'form': form, 'formset': formset})
    
class FetchStudentsView(View):
    
    @staticmethod
    def getCourseId( kwargs):
        if "course_id" in kwargs:
            return kwargs["course_id"]
        elif "code_ue" in kwargs:
            code_ue = kwargs["code_ue"]
            year = kwargs["year"] if "year" in kwargs else VUtilitiesService.getCurrentYear()
            course = get_object_or_404(Course, code_ue=code_ue, year=year)
            return course.id
        
    def get(self, request, *args, **kwargs):
        course_id = FetchStudentsView.getCourseId(kwargs)
        course = Course.objects.get(id=course_id)
        study_field = course.study_field
        study_level = course.study_level
        notes = NoteModel.objects.filter(course_id=course_id)
        students = Users.objects.filter(study_level =study_level, study_field = study_field)
        student_data = [{"username": student.username, "name": f"{student.first_name} {student.last_name}"} for student in students]
        student_data = list()
        for student in students:
            _student = {
                "username" : student.username,
                "name": f"{student.first_name} {student.last_name}",
            }
            _notes = notes.filter(student = student)
            if(_notes):
                _student["note"] = notes[0].note
            student_data.append(_student) 
        return JsonResponse(student_data, safe=False)
    
class SubmitNotesView(View):
    template_name = 'course_manager/submit_notes.html'
    
    
    def post(self, request, *args, **kwargs):
        course_id = FetchStudentsView.getCourseId(kwargs)
        try:
            values = list()
            notes_data = json.loads(request.body)  # Assuming request body contains JSON data
            for note_data in notes_data:
                student = Users.objects.get(username=note_data['username'])
                print(note_data)
                note = NoteModel(
                    course_id=course_id,
                    student=student,
                    correcteur=request.user,
                    note=note_data['note'],
                    # note_type_id=1  # Adjust this as needed
                )
                note.save()
                values.append(note.id)
            return JsonResponse({"status": "success", "data": values})
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An error occurred. {str(e)}"}, status=500)
    def get(self, request, *args, **kwargs):
        course_id = FetchStudentsView.getCourseId(kwargs)
        course = get_object_or_404(Course, id=course_id)
        context = {'courseLabel': course.label, "course_id": course_id}
        return render(request, self.template_name, context)
    
    
class SubmitNotesPageView(LoginBaseViews):

    def get(self, request, *args, **kwargs):
        course_id = FetchStudentsView.getCourseId(kwargs)
        course = get_object_or_404(Course, id=course_id)
        context = {'courseLabel': course.label, "course_id": course_id}
        return render(request, self.template_name, context)
    
class RegisterView(View):
    template_name = 'v_utilities/form-base.html'
    form_class = AdminCourseForm

    def get(self, request):
        form = self.form_class()
        print(f"json form: {form.fields}")
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})