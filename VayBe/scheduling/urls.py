from django.urls import path
from . import views

urlpatterns = [
    path('generate-schedule/', views.generate_schedule, name='generate_schedule'),
    path('view-schedules/', views.view_schedules, name='view_schedules'),
]

urlpatterns += [
    path('rooms/', views.list_rooms, name='list_rooms'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/update/<str:room_id>/', views.update_room, name='update_room'),
    path('rooms/delete/<str:room_id>/', views.delete_room, name='delete_room'),
]
