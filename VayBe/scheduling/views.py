from django.shortcuts import render, redirect
from django.http import JsonResponse
from .services import SchedulingService

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
    response = None
    if request.method == 'POST':
        schedule_request = {
            "granularity": int(request.POST.get('granularity')),
            "courses": [],  # Add course details as needed
            "weekdays": [1, 2, 3, 4, 5],
            "rooms": {},  # Add room details as needed
            "schoolClasses": {}  # Add school class details as needed
        }
        response = SchedulingService.generate_schedule(schedule_request)
    return render(request, 'generate_schedule.html', {'response': response})

# View all schedules
def view_schedules(request):
    schedules = SchedulingService.get_all_schedules()
    return JsonResponse(schedules, safe=False)
