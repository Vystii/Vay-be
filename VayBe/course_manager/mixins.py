from django.contrib.auth.mixins import AccessMixin
# from django.core.exceptions import PermissionDenied
from .permissions import IsTeachingOrPermissionDenied  # Import your custom permission

class IsTeacherPermissionRequiredMixin(AccessMixin):
    permission_class = IsTeachingOrPermissionDenied

    def dispatch(self, request, *args, **kwargs):
        if not self.permission_class().has_permission(request, self):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
