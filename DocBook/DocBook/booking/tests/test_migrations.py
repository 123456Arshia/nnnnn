from django.test import TestCase
from booking.models import Admin, Schedule, Doctor, Review, Patient, Appointment, Notification, DoctorProfile
from django.utils import timezone
from django.contrib.auth.models import User

class MigrationTestCase(TestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(username='admin_tester', password='admin')
        self.admin = Admin.objects.create(user=self.user_admin)
        self.schedule = Schedule.objects.create(day='Monday', start_time=timezone.now().time(), end_time=timezone.now().time())
        self.doctor_user = User.objects.create_user(username='doc_test', password='password')
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user, specialization='cardiology')
        self.patient_user = User.objects.create_user(username='patient_test', password='password')
        self.patient = Patient.objects.create(user=self.patient_user, medical_history='None')
        self.appointment = Appointment.objects.create(doctor=self.doctor_profile, patient=self.patient, date_time=timezone.now(), status='Pending')
        self.notification = Notification.objects.create(user=self.patient_user, message='Test notification')
        self.doctor_legacy = Doctor.objects.create(name='Dr. Legacy', specialization='cardiology')
        self.review = Review.objects.create(doctor=self.doctor_legacy, rating=5, comment='Excellent!')

    def test_migrations(self):
        self.assertEqual(self.schedule.day, 'Monday')
        self.assertEqual(self.admin.user.username, 'admin_tester')
        self.assertEqual(self.doctor_profile.user.username, 'doc_test')
        self.assertEqual(self.patient.user.username, 'patient_test')
        self.assertEqual(self.appointment.status, 'Pending')
        self.assertEqual(self.notification.message, 'Test notification')
        self.assertEqual(self.doctor_legacy.name, 'Dr. Legacy')
        self.assertEqual(self.review.rating, 5)
