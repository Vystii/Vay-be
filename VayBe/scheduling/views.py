import random
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import SchoolClass
from .services import SchedulingService
from course_manager.models import Course
# List all rooms
def list_rooms(request):
    rooms = SchedulingService.get_all_rooms()
    print(rooms)
    return render(request, 'scheduling/list_rooms.html', {'rooms': rooms})

# Create a new room
def create_room(request):
    if request.method == 'POST':
        room_data = {
            'id': request.POST.get('id'),  # Include room id
            'name': request.POST.get('name'),
            'capacity': request.POST.get('capacity')
        }
        SchedulingService.create_room(room_data)
        return redirect('list_rooms')
    return render(request, 'scheduling/create_room.html')

# Update an existing room
def update_room(request, room_id):
    room = SchedulingService.get_room(room_id)
    if request.method == 'POST':
        room_data = {
            'id': room_id,  # Include room id
            'name': request.POST.get('name'),
            'capacity': request.POST.get('capacity')
        }
        SchedulingService.update_room(room_id, room_data)
        return redirect('list_rooms')
    return render(request, 'scheduling/update_room.html', {'room': room})

# Delete a room
def delete_room(request, room_id):
    """shoud implement the delete method instead of get and post
    """
    if request.method == 'POST' or request.method=='GET':
        SchedulingService.delete_room(room_id)
        return redirect('list_rooms')
    room = SchedulingService.get_room(room_id)
    return render(request, 'scheduling/delete_room.html', {'room': room})

# Generate schedule
def generate_schedule(request):
    courses = Course.objects.all()
    schoolClasses = SchoolClass.objects.all()
    response = None
    if request.method == 'POST':
        schedule_request = {
            "granularity": int(request.POST.get('granularity')),
            "courses": [
                {
                    "id": course.id,
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
            }  # Add school class details as needed
        }
        print(schedule_request)
        response = SchedulingService.generate_schedule(schedule_request)
    return render(request, 'scheduling/generate_schedule.html', {'response': response})

# View all schedules
def view_schedules(request):
    schedules = SchedulingService.get_all_schedules()
    return JsonResponse(schedules, safe=False)
