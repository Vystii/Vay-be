from django.urls import path
from .views import (
    ListRoomsView,
    CreateRoomView,
    UpdateRoomView,
    DeleteRoomView,
    GenerateScheduleView,
    ViewSchedulesView,
    AddScheduleView,
    GetCoursesSchedulesView,
    DeleteScheduleView,
    GetSchoolClassesView,
    GetCoursesView,
    ManageSchedulesView,
    GetSettingsView,
)

urlpatterns = [
    # API endpoints for Django side data
    path('api/school-classes/', GetSchoolClassesView.as_view(), name='get_school_classes'),
    path('api/courses/', GetCoursesView.as_view(), name='get_courses'),
    
    # Routes for room management
    path('api/rooms/', ListRoomsView.as_view(), name='list_rooms'),
    path('api/rooms/create/', CreateRoomView.as_view(), name='create_room'),
    path('api/rooms/update/<str:room_id>/', UpdateRoomView.as_view(), name='update_room'),
    path('api/rooms/delete/<str:room_id>/', DeleteRoomView.as_view(), name='delete_room'),

    # Routes for schedule management
    path('api/schedules/', ViewSchedulesView.as_view(), name='view_schedules'),
    path('api/schedules/add/', AddScheduleView.as_view(), name='add_schedule'),
    path('api/schedules/delete/<int:schedule_id>/', DeleteScheduleView.as_view(), name='delete_schedule'),
    
    # Route for generating schedules
    path('api/schedules/generate/', GenerateScheduleView.as_view(), name='generate_schedule'),
    path('api/get-courses-schedules', GetCoursesSchedulesView.as_view(), name='course_schedules'),

    # Route for the Vue.js template view
    path('manage-schedules/', ManageSchedulesView.as_view(), name='manage_schedules'),

    # Route for retrieving settings
    path('api/settings/<int:settings_id>/', GetSettingsView.as_view(), name='get_settings'),
]
