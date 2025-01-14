from booking.models import Admin, Schedule, Doctor, Review, Patient, Appointment, Notification
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

        # Create regular users and patients
        user1 = User.objects.create_user(username="john_doe", password="password123")
        user2 = User.objects.create_user(username="john_dox", password="password123")

        # Ensure that the Patient model gets a non-null User
        patient1 = Patient.objects.create(user=user1, medical_history="Diabetes, Hypertension")
        patient2 = Patient.objects.create(user=user2, medical_history="No significant history")

        # Create schedules
        schedule1 = Schedule.objects.create(day="Monday", start_time="09:00", end_time="17:00")
        schedule2 = Schedule.objects.create(day="Tuesday", start_time="10:00", end_time="16:00")
        schedule3 = Schedule.objects.create(day="Wednesday", start_time="08:00", end_time="15:00")

        # Create doctors
        doctor1 = Doctor.objects.create(name="Dr. Alice Smith", specialization="cardiology", schedule=schedule1)
        doctor2 = Doctor.objects.create(name="Dr. Jane Taylor", specialization="neurology", schedule=schedule3)

        # Create appointments
        Appointment.objects.create(
            doctor=doctor1, patient=patient1, date_time=now() + timedelta(days=1), status="Pending"
        )
        Appointment.objects.create(
            doctor=doctor2, patient=patient2, date_time=now() + timedelta(days=3), status="Confirmed"
        )

        # Create reviews
        Review.objects.create(doctor=doctor1, rating=5, comment="Excellent care and attention.")
        Review.objects.create(doctor=doctor2, rating=4, comment="Great diagnosis and treatment.")

        # Create notifications
        Notification.objects.create(user=user1, message="Your appointment with Dr. Alice Smith is pending.")
        Notification.objects.create(user=user2, message="Your appointment with Dr. John Doe is confirmed.")

        self.stdout.write(self.style.SUCCESS("Test data populated successfully!"))
