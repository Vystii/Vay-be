from django.urls import path

from . import views

urlpatterns = [
    # path("", views.requ, name="index"),
    path("get-courses", views.GetCourse.as_view(), name="user_courses"),
    path("my-request", views.MyRequestsPage.as_view(), name = "user_request"),
    path('login', views.CustomLoginView.as_view(), name='loginV2'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('register/', views.RegisterView.as_view(), name='register'),
]