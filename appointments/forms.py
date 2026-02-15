from django import forms
from .models import Appointment
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean_appointment_date(self):
            appointment_date = self.cleaned_data.get('appointment_date')

            if appointment_date < timezone.now():
                raise forms.ValidationError("You cannot create an appointment in the past.")

            return appointment_date