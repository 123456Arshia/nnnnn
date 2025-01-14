from collections import defaultdict
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import time
from datetime import datetime, timedelta


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.user.username


class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Saturday', 'Sat'),
        ('Sunday', 'Sun'),
        ('Monday','Mon'),
        ('Tuesday','Tue'),
        ('Wednesday', 'Wed'),
    ]

    day = models.CharField(max_length=50, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(default=time(16, 0))
    end_time = models.TimeField(default=time(21, 0))

    def __str__(self):
        return f"{self.day} ({self.start_time} - {self.end_time})"


class Doctor(models.Model):
    SPECIALIZATIONS = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('general_practice', 'General Practice'),
        ('psychiatry', 'Psychiatry'),
    ]

    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS)

    def __str__(self):
        return f"{self.name} ({self.get_specialization_display()})"

    @staticmethod
    def search_doctors(criteria):
        if not criteria.strip():
            return Doctor.objects.all()  # Return all doctors if no criteria
        return Doctor.objects.filter(
            Q(name__icontains=criteria) | Q(specialization__icontains=criteria)
        )

    @staticmethod
    def get_available_slots(self):
        available_slots = defaultdict(list)
        today = timezone.localdate()
        current_time = timezone.localtime().time()

        # Define the slots (16:00 - 21:00, every 30 minutes)
        for day_offset in range(7):  # For the next 7 days (Saturday to Friday)
            day = today + timedelta(days=day_offset)
            if day.weekday() == 5:  # Saturday
                for hour in range(16, 22):  # From 16:00 to 22:00
                    for minute in [0, 30]:
                        slot_time = timezone.datetime.combine(day, timezone.time(hour, minute))
                        available_slots[day].append(slot_time)
        return available_slots

    def get_specialization_display(self):
        return self.specialization

    def get_reserved_slots(self):
        reserved_slots = {}
        appointments = Appointment.objects.filter(doctor=self, status='Confirmed')
        for appointment in appointments:
            day = appointment.date_time.strftime('%A')
            time = appointment.date_time.strftime('%H:%M')
            reserved_slots.setdefault(day, []).append(time)
        return reserved_slots


class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.doctor.name}: {self.rating} Stars"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, default=1)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def book_appointment(self, doctor, date_time):
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=self,
            date_time=date_time,
            status='Pending'
        )
        return appointment

    def view_reviews(self):
        reviews = Review.objects.filter(doctor__appointment__patient=self)
        return reviews

    def manage_account(self, new_medical_history=None, new_user_info=None):
        if new_medical_history:
            self.medical_history = new_medical_history

        if new_user_info:
            self.user.first_name = new_user_info.get("first_name", self.user.first_name)
            self.user.last_name = new_user_info.get("last_name", self.user.last_name)
            self.user.email = new_user_info.get("email", self.user.email)
            self.user.save()

        self.save()
        print(f"Account for {self.user.username} updated successfully!")


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.patient.user.username} with {self.doctor.name} on {self.date_time}"

    @classmethod
    def reserve_slot(cls, doctor, patient, date_time):
        if cls.objects.filter(doctor=doctor, date_time=date_time, status='Confirmed').exists():
            raise ValueError("Slot is already reserved.")

        if cls.objects.filter(doctor=doctor, patient=patient, status='Confirmed').exists():
            raise ValueError("You already have a reserved slot with this doctor.")

        if cls.objects.filter(patient=patient, date_time=date_time, status='Confirmed').exists():
            raise ValueError("You cannot reserve appointments with two doctors at the same time.")

        appointment = cls.objects.create(
            doctor=doctor,
            patient=patient,
            date_time=date_time,
            status='Confirmed'
        )
        Notification.send_notification(patient.user, doctor, date_time)
        return appointment


class Notification(models.Model):
    message = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=1)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    @classmethod
    def send_notification(cls, patient, doctor, appointment_time):
        message = f"Appointment with {doctor.name} on {appointment_time} confirmed."
        notification = cls.objects.create(
            message=message,
            date_time=appointment_time,
            user=patient
        )
        print(f"Notification sent to user: {patient.username}")
        return notification