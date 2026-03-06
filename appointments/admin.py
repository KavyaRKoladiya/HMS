# Register your models here.
from django.contrib import admin
from .models import Appointment, AppointmentDocument

admin.site.register(Appointment)
admin.site.register(AppointmentDocument)
