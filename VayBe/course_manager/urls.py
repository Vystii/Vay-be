from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("courses/<str:user_matricule>", views.UserCourses.as_view(), name="user_course"),
    path("courses/<int:year>/<str:study_field>/<str:study_level>", views.ClassCourses.as_view(), name="class_course"),
    path("notes", views.Note.as_view(), name="course"),
    
]