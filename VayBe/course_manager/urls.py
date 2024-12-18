from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("courses/<str:user_matricule>", views.UserCourses.as_view(), name="user_course"),
    path("my-courses/", views.CoursesPage.as_view(), name="user_course_page"),
    path("courses/<int:year>/<str:study_field>/<str:study_level>", views.ClassCourses.as_view(), name="class_course"),
    path("notes", views.Note.as_view(), name="course"),
    path('course/<int:year>/<str:code_ue>', views.CourseDetailView.as_view(), name='course_detail')
]