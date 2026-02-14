from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm

@login_required
def patient_list(request):
    query = request.GET.get('q')

    if query:
        patients = Patient.objects.filter(first_name__icontains=query) | \
                   Patient.objects.filter(last_name__icontains=query)
    else:
        patients = Patient.objects.all()

    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
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

@login_required
def patient_delete(request, pk):
    patient = Patient.objects.get(id=pk)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
