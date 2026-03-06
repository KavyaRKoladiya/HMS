from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()

    def clean(self):
        # Doctor cannot have two appointments at same time
        if Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date=self.appointment_date
        ).exclude(id=self.id).exists():
            raise ValidationError("This doctor already has an appointment at this time.")

        # Patient cannot have two appointments at same time
        if Appointment.objects.filter(
            patient=self.patient,
            appointment_date=self.appointment_date
        ).exclude(id=self.id).exists():
            raise ValidationError("This patient already has an appointment at this time.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_time'
            ),
            models.UniqueConstraint(
                fields=['patient', 'appointment_date'],
                name='unique_patient_appointment_time'
            ),
        ]

    def __str__(self):
        return f"Appointment - {self.patient} with {self.doctor}"


class AppointmentDocument(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    uploaded_by = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Doctor who uploaded this document"
    )
    file = models.FileField(upload_to='documents/')
    description = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.appointment} ({self.upload_date:%Y-%m-%d})"
