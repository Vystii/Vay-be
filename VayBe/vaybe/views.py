# vaybe/views.py
from django.shortcuts import redirect

def custom_404_view(request, exception):
    return redirect('login')
