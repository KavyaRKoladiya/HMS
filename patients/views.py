
from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'patients/patient_form.html', {'form': form})

def patient_update(request, pk):
    patient = Patient.objects.get(id=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/patient_form.html', {'form': form})


def patient_delete(request, pk):
    patient = Patient.objects.get(id=pk)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
