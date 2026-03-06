from django import forms
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
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


class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        # only ask for email and password; username will be set automatically
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # username field is not exposed at all, so nothing to hide

    def clean(self):
        # run parent cleaning, then perform email-specific checks below
        cleaned = super().clean()
        email = cleaned.get('email')
        if email:
            # copy email to username so downstream logic sees it
            cleaned['username'] = email
        return cleaned


    def clean_email(self):
        email = self.cleaned_data.get('email')
        # doctor record must exist and not already linked
        try:
            doctor = Doctor.objects.get(email__iexact=email)
        except Doctor.DoesNotExist:
            raise forms.ValidationError('No doctor record found with this email.')
        if doctor.user is not None:
            raise forms.ValidationError('An account has already been created for this doctor.')
        return email

    def _post_clean(self):
        # run normal post_clean to perform model validation and unique checks
        super()._post_clean()
        # if username uniqueness triggered an error but a User already exists,
        # we actually allow reuse instead of complaining.
        if 'username' in self.errors:
            email = self.cleaned_data.get('email')
            if email and User.objects.filter(username=email).exists():
                # drop the username error so the form can be considered valid
                del self.errors['username']

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        # attempt to reuse an existing User if one is already present
        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email}
        )

        # set/override password each time form is saved
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()

        # link to doctor profile
        doctor = Doctor.objects.get(email__iexact=email)
        doctor.user = user
        doctor.save()
        # ensure doctor group membership
        group, _ = Group.objects.get_or_create(name='Doctor')
        user.groups.add(group)
        return user
