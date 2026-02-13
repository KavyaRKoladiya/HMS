from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/appointment_form.html', {'form': form})


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


def appointment_delete(request, pk):
    appointment = Appointment.objects.get(id=pk)

    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')

    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})
