from django.contrib import admin
from .models import Admin, Schedule, Doctor, Patient, Appointment, Notification, Review

admin.site.register(Admin)
admin.site.register(Schedule)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Notification)
admin.site.register(Review)
