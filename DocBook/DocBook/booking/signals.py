from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Doctor

@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    """
    Example: If your project uses a 'Doctor' group,
    and you want to automatically create a Doctor profile
    when a user is assigned to that group.
    """
    if created and instance.groups.filter(name='Doctor').exists():
        Doctor.objects.create(user=instance, name=instance.username, specialization='general_practice')

@receiver(post_save, sender=User)
def save_doctor_profile(sender, instance, **kwargs):
    if hasattr(instance, 'doctor'):
        instance.doctor.save()
