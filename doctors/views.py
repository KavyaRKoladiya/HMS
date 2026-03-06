from django.contrib.auth.decorators import login_required
from hms.decorators import role_required
from django.shortcuts import render, redirect
from .models import Doctor
from .forms import DoctorForm, DoctorRegistrationForm

from django.utils import timezone
from appointments.models import Appointment, AppointmentDocument
from appointments.forms import AppointmentDocumentForm
from django.shortcuts import get_object_or_404

@login_required
@role_required(['Admin', 'Receptionist', 'Doctor'])
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

@login_required
@role_required(['Admin'])
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()

    return render(request, 'doctors/doctor_form.html', {'form': form})

@login_required
@role_required(['Admin'])
def doctor_update(request, pk):
    doctor = Doctor.objects.get(id=pk)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'doctors/doctor_form.html', {'form': form})

@login_required
@role_required(['Admin'])
def doctor_delete(request, pk):
    doctor = Doctor.objects.get(id=pk)

    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')

    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})


@login_required
@role_required(['Doctor'])
def doctor_history(request):
    # identify doctor profile linked to user
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        # fallback by email
        doctor = Doctor.objects.filter(email=request.user.email).first()

    if not doctor:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Doctor profile not found for the current user.")

    now = timezone.now()
    past_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__lt=now
    ).order_by('-appointment_date')

    upload_form = AppointmentDocumentForm()

    # handle upload POST from history page
    if request.method == 'POST':
        form = AppointmentDocumentForm(request.POST, request.FILES)
        appointment_id = request.POST.get('appointment_id')
        if form.is_valid() and appointment_id:
            doc = form.save(commit=False)
            doc.appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
            doc.uploaded_by = doctor
            doc.save()
            return redirect('doctor_history')
        else:
            upload_form = form

    return render(
        request,
        'doctors/doctor_history.html',
        {
            'doctor': doctor,
            'past_appointments': past_appointments,
            'upload_form': upload_form,
        }
    )


def doctor_register(request):
    # allow doctors to claim their account by email and set password
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = DoctorRegistrationForm()

    return render(request, 'doctors/doctor_register.html', {'form': form})
