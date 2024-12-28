from django.urls import path
from . import views

urlpatterns = [
    # API endpoints for Django side data
    path('api/school-classes/', views.get_school_classes, name='get_school_classes'),
    path('api/courses/', views.get_courses, name='get_courses'),
    
    # Routes for room management
    path('api/rooms/', views.list_rooms, name='list_rooms'),
    path('api/rooms/create/', views.create_room, name='create_room'),
    path('api/rooms/update/<str:room_id>/', views.update_room, name='update_room'),
    path('api/rooms/delete/<str:room_id>/', views.delete_room, name='delete_room'),

    # Routes for schedule management
    path('api/schedules/', views.view_schedules, name='view_schedules'),
    path('api/schedules/add/', views.add_schedule, name='add_schedule'),
    path('api/schedules/delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    
    # Route for generating schedules
    path('api/schedules/generate/', views.generate_schedule, name='generate_schedule'),

    # Route for the Vue.js template view
    path('manage-schedules/', views.manage_schedules, name='manage_schedules'),

    # Route for retrieving settings
    path('api/settings/<int:settings_id>/', views.get_settings, name='get_settings'),
]
