from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse as HttpResponse
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.views import LoginView
from django.views import View
from v_utilities.views import LoginBaseViews, TemplateBaseViews
from course_manager.views import UserCourses
from django.contrib import messages
from .models import SchoolRequestFile, Users, SchoolRequest
from .forms import CustomUserCreationForm, SchoolRequestFileForm, SchoolRequestForm
from .dashboard_block.plugin_manager import PluginManager
from django.db.models import Q
import json

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
        context['blocks'] = PluginManager.getBlocksInfos(self.request.user.is_superuser and not self.request.user.is_staff)
        return context

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

class RequestDetailView(LoginBaseViews):
    template_name = "users/request-details.html"
    context_object_name = 'request'

    def get(self, request,  pk):
        datas = self.get_context_data(pk)
        
        return render(request, self.template_name, datas)

    def post(self, request, pk):
        school_request_instance = get_object_or_404(SchoolRequest, pk=pk)
        form = SchoolRequestForm(request.POST, instance=school_request_instance)
        CourseFileFormSet = modelformset_factory(SchoolRequestFile, form=SchoolRequestFileForm, extra=10)
        
        formset = CourseFileFormSet(request.POST, request.FILES, queryset=SchoolRequestFile.objects.filter(school_request=school_request_instance))
        if form.is_valid() and formset.is_valid():
            form.save()
            filesForm = formset.save(commit=False)
            
            for fileForm in filesForm:
                fileForm.school_request = school_request_instance
                fileForm.save()
            datas = self.get_context_data(pk)
        else:
            datas = self.get_context_data(pk)
            datas['formset']['form'] = form
            datas['formset']['fileForm'] = form
            
        datas['formset']['form'] = form
        return render(request, self.template_name, datas)

    def get_context_data(self, pk):
        user = self.request.user
        schoolRequest = get_object_or_404(SchoolRequest, pk=pk)
        form = SchoolRequestForm(instance=schoolRequest)
        CourseFileFormSet = modelformset_factory(SchoolRequestFile, form=SchoolRequestFileForm, extra=1)
        files = SchoolRequestFile.objects.filter(school_request=schoolRequest)
        fileForm = CourseFileFormSet(queryset=files)
        return {
            "isTeacher": user.user_permissions.filter(codename='teach').exists() or user.is_superuser,
            "can_edit":True if True else schoolRequest["sender"]["username"] == user.username,
            "modal_id": "form_edit_request",
            "ent_request": schoolRequest.toDict(True),
            "formset": {"form": form,  "fileForm": fileForm}
        }


class MyRequestsPage(TemplateBaseViews):
    template_name = "v_utilities/dashboard-table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Check if the user has the 'teach' permission or is a superuser
        isTeacher = user.user_permissions.filter(codename='teach').exists() or user.is_superuser
        context['isTeacher'] = isTeacher

        # Retrieve SchoolRequest objects where the user is either owner or receiver
        school_requests = SchoolRequest.objects.filter(Q(owner=user) | Q(receiver=user))
        source_url = reverse("user_request",)  # Assuming you have a URL pattern for fetching data

        # Table settings
        tableSettings = {
            "actions": [
                {"label": "action1", "class": "url", "token": "action1"},
                {"label": "action2", "class": "url", "token": "action2"},
            ],
            "table_header": [
                {"label": "ID", "id": "id"},
                {"label": str(_("Receiver")), "id": "receiver"},
                {"label": str(_("Sender")), "id": "sender"},
                {"label": str(_("Processed")), "id": "processed"},
            ]
        }
        context.update({
            "header": {"title": _("Your Requests")},
            "data_source": source_url,
            "tableSettings": tableSettings,
            "jsonSettings": json.dumps(tableSettings),
            'school_requests': school_requests
        })
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        school_requests = SchoolRequest.objects.filter(Q(owner=user) | Q(receiver=user))
        school_requests_data = [request.toDict() for request in school_requests]
        return JsonResponse(school_requests_data, safe=False)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
            # login(request, user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class RegisterView(View):
    template_name = 'v_utilities/form-base.html'
    form_class = CustomUserCreationForm

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