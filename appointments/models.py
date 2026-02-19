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
