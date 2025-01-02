from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("courses/<str:user_matricule>", views.UserCourses.as_view(), name="user_course"),
    path("my-courses/", views.CoursesPage.as_view(), name="user_course_page"),
    path("courses/<int:year>/<str:study_field>/<str:study_level>", views.ClassCourses.as_view(), name="class_course"),
    path("notes", views.Note.as_view(), name="course"),
    path('course/<int:year>/<str:code_ue>', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/<course_id>', views.CourseDetailView.as_view(), name='course_détails_id'),
    path('create-course/', views.CourseCreateView.as_view(), name='create_course'),
]
urlpatterns += [ # Other URL patterns... 
    path('api/students/<int:course_id>/', views.FetchStudentsView.as_view(), name='get_students'), 
    path('api/students/<int:year>/<str:code_ue>', views.FetchStudentsView.as_view(), name='get_students'), 
]
urlpatterns += [ path('submit_notes/<int:course_id>/', views.SubmitNotesView.as_view(), name='submit_notes_page'), ]