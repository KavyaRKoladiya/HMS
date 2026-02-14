from django.shortcuts import render

from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required


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

@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
    }

    return render(request, 'dashboard.html', context)


