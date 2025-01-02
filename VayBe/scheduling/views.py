from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from v_utilities.views import LoginBaseViews, TemplateBaseViews
from course_manager.views import UserCourses
from .models import SchoolClass
from .services import SchedulingService
from course_manager.models import Course

class ListRoomsView(View):
    def get(self, request: WSGIRequest):
        rooms = SchedulingService.get_all_rooms()
        return render(request, 'scheduling/list_rooms.html', {'rooms': rooms})

class CreateRoomView(View):
    def get(self, request: WSGIRequest):
        return render(request, 'scheduling/create_room.html')
    
    def post(self, request: WSGIRequest):
        room_data = {
            'id': request.POST.get('id'),
            'name': request.POST.get('name'),
            'capacity': request.POST.get('capacity')
        }
        SchedulingService.create_room(room_data)
        return redirect('list_rooms')

class UpdateRoomView(View):
    def get(self, request: WSGIRequest, room_id):
        room = SchedulingService.get_room(room_id)
        return render(request, 'scheduling/update_room.html', {'room': room})
    
    def post(self, request: WSGIRequest, room_id):
        room_data = {
            'id': room_id,
            'name': request.POST.get('name'),
            'capacity': request.POST.get('capacity')
        }
        SchedulingService.update_room(room_id, room_data)
        return redirect('list_rooms')

class DeleteRoomView(View):
    def get(self, request: WSGIRequest, room_id):
        room = SchedulingService.get_room(room_id)
        return render(request, 'scheduling/delete_room.html', {'room': room})
    
    def post(self, request: WSGIRequest, room_id):
        SchedulingService.delete_room(room_id)
        return redirect('list_rooms')

class GenerateScheduleView(View):
    def get(self, request: WSGIRequest):
        return render(request, 'scheduling/generate_schedule.html', {'response': None, 'test': 'test'})
    
    def post(self, request: WSGIRequest):
        courses = Course.objects.all()
        schoolClasses = SchoolClass.objects.all()
        schedule_request = {
            "granularity": int(request.POST.get('granularity')),
            "courses": [
                {
                    "id": course.code_ue,
                    "level": course.study_level.code,
                    "schoolClassId": f"{course.study_field.code}_{course.study_level.code}"
                } for course in courses
            ],
            "weekdays": [1, 2, 3, 4, 5],
            "schoolClasses": {
                "shouldDeleteSchoolClass": False,
                "data": [
                    {
                        "name": f"{s_class.study_field.code}_{s_class.study_level.code}",
                        "numberOfStudents": s_class.expected_students,
                        "level": s_class.study_level.code        
                    } for s_class in schoolClasses
                ]
            }
        }
        response = SchedulingService.generate_schedule(schedule_request)
        return render(request, 'scheduling/generate_schedule.html', {'response': response, "test": "test"})

class ViewSchedulesView(View):
    def post(self, request: WSGIRequest):
        schedules = SchedulingService.get_all_schedules()
        return JsonResponse(schedules, safe=False)

class AddScheduleView(View):
    def get(self, request: WSGIRequest):
        return render(request, 'scheduling/add_schedule.html')
    
    def post(self, request: WSGIRequest):
        classe = SchoolClass.objects.get(pk=request.POST.get('class_id'))
        course = Course.objects.get(pk=(request.POST.get('course_id')))
        schedule_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'classId': classe.buildId(),
            'courseId': course.code_ue
        }
        room_id = request.POST.get("room_id")
        SchedulingService.add_schedule(schedule_data, room_id)
        return redirect('view_schedules')
        
class GetCoursesSchedulesView(View):
    def post(self, request: WSGIRequest):
        # ids = request.POST.get("course_ids")
        courses = UserCourses.getCourses(request.user.username)
        ids = [course["id"] for course in courses]
        if not ids:
            return JsonResponse({})
        schedules = SchedulingService.get_courses_schedules(ids)
        return JsonResponse(schedules, safe=False)

class DeleteScheduleView(View):
    def get(self, request: WSGIRequest, schedule_id):
        schedule = SchedulingService.get_schedule_by_id(schedule_id)
        return render(request, 'scheduling/delete_schedule.html', {'schedule': schedule})
    
    def post(self, request: WSGIRequest, schedule_id):
        SchedulingService.delete_schedule(schedule_id)
        return redirect('view_schedules')

class GetSchoolClassesView(View):
    def get(self, request: WSGIRequest):
        classes = list(SchoolClass.objects.values())
        return JsonResponse(classes, safe=False)

class GetCoursesView(View):
    def get(self, request: WSGIRequest):
        courses = list(Course.objects.values())
        return JsonResponse(courses, safe=False)

class ManageSchedulesView(TemplateBaseViews):
    template_name = 'scheduling/manage_schedules.html'
    # def get(self, request: WSGIRequest):
        # return render(request, '')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user.toDict())
        context["url"] = reverse("course_schedules")
        return context

class GetSettingsView(View):
    def get(self, request: WSGIRequest, settings_id):
        try:
            settings = SchedulingService.get_settings(settings_id)
            return JsonResponse(settings, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
