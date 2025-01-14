from booking.models import Admin, Schedule, Doctor, Review, Patient, Appointment, Notification, DoctorProfile
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Populate the database with test data."

    def handle(self, *args, **kwargs):
        # Create admin user if not exists
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin123"
            )
            Admin.objects.create(user=admin_user)
        else:
            admin_user = User.objects.get(username="admin")
            print("Admin user already exists.")

        # Create a sample doctor user and DoctorProfile
        if not User.objects.filter(username="doctor1").exists():
            doctor_user = User.objects.create_user(username="doctor1", password="docpass123", first_name="Alice", last_name="Smith")
            DoctorProfile.objects.create(user=doctor_user, specialization="cardiology")
        else:
            doctor_user = User.objects.get(username="doctor1")

        # Create a sample patient user
        if not User.objects.filter(username="john_doe").exists():
            user1 = User.objects.create_user(username="john_doe", password="password123")
            Patient.objects.create(user=user1, medical_history="Diabetes, Hypertension")
        else:
            user1 = User.objects.get(username="john_doe")

        # Create schedules
        schedule1 = Schedule.objects.create(day="Monday", start_time="09:00", end_time="17:00")
        schedule2 = Schedule.objects.create(day="Tuesday", start_time="10:00", end_time="16:00")
        schedule3 = Schedule.objects.create(day="Wednesday", start_time="08:00", end_time="15:00")

        # Create older "Doctor" for reference (not necessarily used with new code)
        doc_legacy = Doctor.objects.create(name="doctor1", specialization="cardiology")

        # Create an appointment
        Appointment.objects.create(
            doctor=doctor_user.doctorprofile,
            patient=Patient.objects.get(user=user1),
            date_time=now() + timedelta(days=1),
            status="Pending"
        )

        # Create a review
        Review.objects.create(doctor=doc_legacy, rating=5, comment="Excellent care and attention.")

        # Create notifications
        Notification.objects.create(user=user1, message="Your appointment is pending.")

        self.stdout.write(self.style.SUCCESS("Test data populated successfully!"))
