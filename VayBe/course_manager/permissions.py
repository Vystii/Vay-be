from rest_framework import permissions
from users.models import Users
from django.shortcuts import get_object_or_404

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # get the user from the right model
        currentUser:Users = get_object_or_404(Users, username =request.user.username)

        # Write permissions are only allowed to the owner of the object
        return obj.owner == request.user
    
    
class IsTeachingOrPermissionDenied(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object
        
        return  request.user in obj.teachers.all()