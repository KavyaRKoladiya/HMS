from django import forms
from django.db.models import Q
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone', 'address']

    def clean(self):
        cleaned = super().clean()
        first = cleaned.get('first_name')
        last = cleaned.get('last_name')
        dob = cleaned.get('date_of_birth')
        phone = cleaned.get('phone')

        qs = Patient.objects.all()
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        # Prevent duplicate patient by name + DOB
        if first and last and dob and qs.filter(
            first_name__iexact=first, last_name__iexact=last, date_of_birth=dob
        ).exists():
            raise forms.ValidationError('A patient with this name and date of birth already exists.')

        # Also prevent reusing phone number
        if phone and qs.filter(phone=phone).exists():
            raise forms.ValidationError('A patient with this phone number already exists.')

        return cleaned
