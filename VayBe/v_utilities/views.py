from django import dispatch
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest
from django.http.response import HttpResponse
from typing import Any
from django.views import View


# Create your views here.
class LoginBaseViews(View):
    class meta:
        abstract = True
    
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)