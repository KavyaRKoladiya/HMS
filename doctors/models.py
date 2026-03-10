# Create your models here.
from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    # optional link to an auth user so we can identify the logged-in doctor
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Associate this doctor record with a User account (optional)"
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        # prefer the user's full name when available, but fall back to the
        # stored first/last name if the user record doesn't have those fields
        if self.user:
            full = self.user.get_full_name().strip()
            if full:
                return f"Dr. {full}"
        # user is missing or has no name; use the doctor model fields
        return f"Dr. {self.first_name} {self.last_name}"


# ensure that whenever a doctor gets a linked user, the user is placed in the
# Doctor group so permissions/decorators work correctly.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(post_save, sender='doctors.Doctor')
def add_user_to_group(sender, instance, **kwargs):
    if instance.user:
        group, _ = Group.objects.get_or_create(name='Doctor')
        instance.user.groups.add(group)
