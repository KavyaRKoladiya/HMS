from django.contrib.auth.decorators import login_required
from hms.decorators import role_required

from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from django.utils import timezone
from django.db.models import Q

@login_required
@role_required(['Admin', 'Receptionist', 'Doctor'])
def appointment_list(request):
    now = timezone.now()
    doctor_id = request.GET.get('doctor')

    appointments = Appointment.objects.all()

    # Apply doctor filter if selected
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    # Split into upcoming & past AFTER filtering
    upcoming_appointments = appointments.filter(
        appointment_date__gte=now
    ).order_by('appointment_date')

    past_appointments = appointments.filter(
        appointment_date__lt=now
    ).order_by('-appointment_date')

    from doctors.models import Doctor
    doctors = Doctor.objects.all()

    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'doctors': doctors,
    }

    return render(request, 'appointments/appointment_list.html', context)

@login_required
@role_required(['Admin', 'Receptionist'])
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
@role_required(['Admin', 'Receptionist'])
def appointment_update(request, pk):
    appointment = Appointment.objects.get(id=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
@role_required(['Admin', 'Receptionist'])
def appointment_delete(request, pk):
    appointment = Appointment.objects.get(id=pk)

    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')

    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})
