"""
URL configuration for vaybe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from v_utilities.views import TemplateBaseViews
from users.views import RequestDetailView
from debug_toolbar.toolbar import debug_toolbar_urls
from .views import custom_404_view


handler404 = custom_404_view
# Add the URL pattern in urls.py
urlpatterns = [
    path('request/<int:pk>', RequestDetailView.as_view(), name="request_page"),
    path('users/', include('users.urls')),
    path('course-manager/', include('course_manager.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path("scheduling/",include("scheduling.urls")) 
] 
urlpatterns += debug_toolbar_urls()
