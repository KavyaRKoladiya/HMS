from django.db.models import Q
from django.contrib.auth.decorators import login_required
from hms.decorators import role_required

from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm

@login_required
@role_required(['Admin', 'Receptionist', 'Doctor'])
def patient_list(request):
    query = request.GET.get('q', '').strip()

    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(first_name__istartswith=query) |
            Q(last_name__istartswith=query)
        )

    # 🔍 Debug lines (temporary)
    print("QUERY:", query)
    print("COUNT:", patients.count())

    context = {
        'patients': patients
    }

    return render(request, 'patients/patient_list.html', context)

@login_required
@role_required(['Admin', 'Receptionist'])
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
@role_required(['Admin', 'Receptionist'])
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
@role_required(['Admin', 'Receptionist'])
def patient_delete(request, pk):
    patient = Patient.objects.get(id=pk)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
