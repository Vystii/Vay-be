import array
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest

from .models import SchoolClass
from .services import SchedulingService
from course_manager.models import Course

# List all rooms
def list_rooms(request: WSGIRequest):
    rooms = SchedulingService.get_all_rooms()
    return render(request, 'scheduling/list_rooms.html', {'rooms': rooms})

# Create a new room
def create_room(request: WSGIRequest):
    if request.method == 'POST':
        room_data = {
            'id': request.POST.get('id'),
            'name': request.POST.get('name'),
            'capacity': request.POST.get('capacity')
        }
        SchedulingService.create_room(room_data)
        return redirect('list_rooms')
    return render(request, 'scheduling/create_room.html')

# Update an existing room
def update_room(request: WSGIRequest, room_id):
    room = SchedulingService.get_room(room_id)
    if request.method == 'POST':
        room_data = {
            'id': room_id,
            'name': request.POST.get('name'),
            'capacity': request.POST.get('capacity')
        }
        SchedulingService.update_room(room_id, room_data)
        return redirect('list_rooms')
    return render(request, 'scheduling/update_room.html', {'room': room})

# Delete a room
def delete_room(request: WSGIRequest, room_id):
    if request.method == 'POST' or request.method == 'GET':
        SchedulingService.delete_room(room_id)
        return redirect('list_rooms')
    room = SchedulingService.get_room(room_id)
    return render(request, 'scheduling/delete_room.html', {'room': room})

# Generate schedule
def generate_schedule(request: WSGIRequest):
    courses = Course.objects.all()
    schoolClasses = SchoolClass.objects.all()
    response = None
    if request.method == 'POST':
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

# View all schedules
def view_schedules(request: WSGIRequest):
    schedules = SchedulingService.get_all_schedules()
    return JsonResponse(schedules, safe=False)

# Add a new schedule
def add_schedule(request: WSGIRequest):
    if request.method == 'POST':
        classe = SchoolClass.objects.get(pk=request.POST.get('class_id'))
        course = Course.objects.get(pk=request.POST.get('course_id'))
        schedule_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'classId': classe.buildId(),
            'courseId': course.code_ue
        }
        room_id = request.POST.get("room_id")
        SchedulingService.add_schedule(schedule_data, room_id)
        return redirect('view_schedules')
    return render(request, 'scheduling/add_schedule.html')

# Remove a specific schedule
def delete_schedule(request: WSGIRequest, schedule_id):
    if request.method == 'POST':
        SchedulingService.delete_schedule(schedule_id)
        return redirect('view_schedules')
    schedule = SchedulingService.get_schedule_by_id(schedule_id)
    return render(request, 'scheduling/delete_schedule.html', {'schedule': schedule})

# API endpoints for Django side data
def get_school_classes(request):
    classes = list(SchoolClass.objects.values())
    return JsonResponse(classes, safe=False)

def get_courses(request):
    courses = list(Course.objects.values())
    return JsonResponse(courses, safe=False)

# Vue.js template view
def manage_schedules(request):
    return render(request, 'scheduling/manage_schedules.html')

def get_settings(request, settings_id):
    try:
        settings = SchedulingService.get_settings(settings_id)
        return JsonResponse(settings, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
