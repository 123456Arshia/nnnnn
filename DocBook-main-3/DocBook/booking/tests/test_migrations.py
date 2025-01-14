from django.test import TestCase
from booking.models import Admin, Schedule, Doctor, Review, Patient, Appointment, Notification
from django.utils import timezone

class MigrationTestCase(TestCase):

    def setUp(self):
        self.schedule = Schedule.objects.create(day='Monday', start_time=timezone.now(), end_time=timezone.now())
        self.admin = Admin.objects.create(username='admin', password='admin')
        self.doctor = Doctor.objects.create(name='Dr. Smith', specialization='cardiology', schedule=self.schedule)
        self.patient = Patient.objects.create(name='John Doe', email='john@example.com', password='password', medical_history='None')
        self.appointment = Appointment.objects.create(doctor=self.doctor, patient=self.patient, date_time=timezone.now())
        self.notification = Notification.objects.create(message='Test notification', date_time=timezone.now(), user=self.patient)
        self.review = Review.objects.create(doctor=self.doctor, rating=5, comment='Excellent!')

    def test_migrations(self):
        self.assertEqual(self.schedule.day, 'Monday')
        self.assertEqual(self.admin.username, 'admin')
        self.assertEqual(self.doctor.name, 'Dr. Smith')
        self.assertEqual(self.patient.email, 'john@example.com')
        self.assertEqual(self.appointment.status, 'Pending')
        self.assertEqual(self.notification.message, 'Test notification')
        self.assertEqual(self.review.rating, 5)
