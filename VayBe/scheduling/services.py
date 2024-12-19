import requests

class SchedulingService:
    BASE_URL = 'http://localhost:8080/api/schedules'
    ROOMS_URL = 'http://localhost:8080/api/rooms'

    @staticmethod
    def generate_schedule(schedule_request):
        url = f'{SchedulingService.BASE_URL}/generate'
        response = requests.post(url, json=schedule_request, params={'deleteExistingSchedules': True})
        return response.json()

    @staticmethod
    def add_schedule(schedule):
        url = f'{SchedulingService.BASE_URL}/add'
        response = requests.post(url, json=schedule)
        return response.json()

    @staticmethod
    def get_schedule_by_id(schedule_id):
        url = f'{SchedulingService.BASE_URL}/get/{schedule_id}'
        response = requests.get(url)
        return response.json()

    @staticmethod
    def get_all_schedules():
        url = f'{SchedulingService.BASE_URL}/get-all'
        response = requests.get(url)
        return response.json()

    @staticmethod
    def delete_schedule(schedule_id):
        url = f'{SchedulingService.BASE_URL}/delete/{schedule_id}'
        response = requests.delete(url)
        return response.status_code

    @staticmethod
    def update_schedule(schedule_id, schedule):
        url = f'{SchedulingService.BASE_URL}/update/{schedule_id}'
        response = requests.put(url, json=schedule)
        return response.json()

    # New methods for room operations
    @staticmethod
    def get_all_rooms():
        url = SchedulingService.ROOMS_URL
        response = requests.get(url)
        return response.json()

    @staticmethod
    def get_room(room_id):
        url = f'{SchedulingService.ROOMS_URL}/{room_id}'
        response = requests.get(url)
        return response.json()

    @staticmethod
    def create_room(room_data):
        url = SchedulingService.ROOMS_URL
        response = requests.post(url, json=room_data)
        return response.json()

    @staticmethod
    def update_room(room_id, room_data):
        url = f'{SchedulingService.ROOMS_URL}/{room_id}'
        response = requests.put(url, json=room_data)
        return response.json()

    @staticmethod
    def delete_room(room_id):
        url = f'{SchedulingService.ROOMS_URL}/{room_id}'
        response = requests.delete(url)
        return response.status_code
