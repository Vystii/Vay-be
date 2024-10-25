from django.http import HttpRequest, HttpResponse
from django.views import View
from .models import Course
from course_manager.models import Course as ModelCourse

class Course(View):
    model = Course
    query_filter ={"status": True}
    
    def alterQuery(self, **args):
        for key in args:
            self.query_filter |= args
        pass
    
    def removeFilter(self, fieldNames:list[str]):
        for field in fieldNames:
            self.query_filter.pop(field, None)
        
    def getCourse(self):
        args = {key: value for key, value in self.query_filter.items() if value is not None}
        course = ModelCourse.objects.filter(**args)
        return course
            
    def get(self, request:HttpRequest):
        user = request.user
        
        return  HttpResponse("Courses")

class Note(View):
    def get(self, request):
        return HttpResponse("notes")    
    
