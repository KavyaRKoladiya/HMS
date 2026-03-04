from django import forms
from django.db.models import Q
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'phone', 'email']

    def clean(self):
        cleaned = super().clean()
        first = cleaned.get('first_name')
        last = cleaned.get('last_name')
        email = cleaned.get('email')
        phone = cleaned.get('phone')

        # Exclude current instance when editing
        qs = Doctor.objects.all()
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        # If email provided and already used, reject
        if email and qs.filter(email__iexact=email).exists():
            raise forms.ValidationError('A doctor with this email already exists.')

        # If phone provided and already used, reject
        if phone and qs.filter(phone=phone).exists():
            raise forms.ValidationError('A doctor with this phone number already exists.')

        # If first+last match and either phone or email match, reject as duplicate
        if first and last and qs.filter(first_name__iexact=first, last_name__iexact=last).filter(
            Q(email__iexact=email) | Q(phone=phone)
        ).exists():
            raise forms.ValidationError('A doctor with these details already exists.')

        return cleaned
