from django.contrib.auth.decorators import login_required
from hms.decorators import role_required
from django.shortcuts import render, redirect
from .models import Doctor
from .forms import DoctorForm

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
