from django.urls import path

from . import views

urlpatterns = [
    # path("", views.requ, name="index"),
    path("get-courses", views.GetCourse.as_view(), name="user_courses")
]