import requests
import json
class SchedulingService:
    BASE_URL = 'http://localhost:8080/api/schedules'
    ROOMS_URL = 'http://localhost:8080/api/rooms'
    SETTINGS_URL = 'http://localhost:8080/api/settings'

    @staticmethod
    def generate_schedule(schedule_request):
        url = f'{SchedulingService.BASE_URL}/generate'
        response = requests.post(url, json=schedule_request, params={'deleteExistingSchedules': True})
        return response.json()

    @staticmethod
    def add_schedule(schedule, room_id: str):
        url = f'{SchedulingService.BASE_URL}/add?roomId={room_id}'
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

    # Methods for room operations
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

    # New method to retrieve settings
    @staticmethod
    def get_settings(settings_id):
        url = f'{SchedulingService.SETTINGS_URL}/1'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_courses_schedules(coursesIds: list[int]):
        print(f"courses_id: {coursesIds}")
        data = json.dumps(coursesIds)
        print(SchedulingService.BASE_URL + "/get-courses-schedules")
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(
            url  = SchedulingService.BASE_URL + "/get-courses-schedules", 
            data = data,
            headers = headers
        )
        # print(response.text)
        return response.json()