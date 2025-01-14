from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from booking.models import Appointment

class Command(BaseCommand):
    help = 'Create user groups for Doctors and Patients'

    def handle(self, *args, **kwargs):
        # Create Doctor group
        doctor_group, created = Group.objects.get_or_create(name='Doctor')
        if created:
            self.stdout.write(self.style.SUCCESS('Doctor group created.'))
        else:
            self.stdout.write('Doctor group already exists.')

        # Optionally assign permissions to Doctor group
        content_type = ContentType.objects.get_for_model(Appointment)
        permissions = Permission.objects.filter(content_type=content_type)
        doctor_group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Permissions assigned to Doctor group.'))

        # Create Patient group
        patient_group, created = Group.objects.get_or_create(name='Patient')
        if created:
            self.stdout.write(self.style.SUCCESS('Patient group created.'))
        else:
            self.stdout.write('Patient group already exists.')
