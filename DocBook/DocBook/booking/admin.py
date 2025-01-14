from django.contrib import admin
from .models import Admin, Schedule, Doctor, Patient, Appointment, Notification, Review

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time')
    list_filter = ('day',)
    search_fields = ('day',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'user')
    search_fields = ('name', 'specialization', 'user__username')
    list_filter = ('specialization',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'medical_history')
    search_fields = ('user__username', 'medical_history')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date_time', 'status')
    list_filter = ('status', 'doctor', 'date_time')
    search_fields = (
        'doctor__name',
        'patient__user__username',
        'status'
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'date_time')
    search_fields = ('user__username', 'message')
    list_filter = ('date_time',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'rating', 'comment')
    search_fields = ('doctor__name', 'comment')
    list_filter = ('rating',)
