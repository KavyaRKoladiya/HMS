from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm

@login_required
def appointment_list(request):
    doctor_id = request.GET.get('doctor')

    if doctor_id:
        appointments = Appointment.objects.filter(doctor_id=doctor_id)
    else:
        appointments = Appointment.objects.all()

    from doctors.models import Doctor
    doctors = Doctor.objects.all()

    context = {
        'appointments': appointments,
        'doctors': doctors,
    }

    return render(request, 'appointments/appointment_list.html', context)

@login_required
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
def appointment_delete(request, pk):
    appointment = Appointment.objects.get(id=pk)

    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')

    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})
