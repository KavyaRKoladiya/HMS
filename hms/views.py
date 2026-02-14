from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'login.html'


def custom_logout(request):
    logout(request)
    return redirect('login')
