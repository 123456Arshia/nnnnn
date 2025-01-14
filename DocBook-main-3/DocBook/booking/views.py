from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import Doctor, Appointment, Notification, Schedule, Patient
from .serializers import AppointmentSerializer, DoctorSerializer, ReviewSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib import messages
from .forms import UserRegistrationForm


def index(request):
    return render(request, 'booking/index.html')

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            medical_history = form.cleaned_data['medical_history']

            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken!')
            else:
                # Check if passwords match
                if password != confirm_password:
                    form.add_error('confirm_password', "Passwords don't match!")
                else:
                    # Create the user and patient profile
                    user = User.objects.create_user(username=username, password=password)
                    Patient.objects.create(user=user, medical_history=medical_history)

                    # Redirect to login page with a success message
                    messages.success(request, 'Your account has been created successfully!')
                    return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'booking/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'booking/login.html')



@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    search_results = []

    if query:
        search_results = Doctor.objects.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query)
        )

    try:
        # Get the logged-in user's appointments
        appointments = Appointment.objects.filter(patient=request.user.patient).order_by('date_time')
    except Appointment.DoesNotExist:
        appointments = []

    return render(request, 'booking/dashboard.html', {
        'appointments': appointments,
        'search_results': search_results,
    })


@login_required
def doctor_details(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user = request.user

    # Time slots & days for the schedule table
    days_of_week = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday']
    time_slots = [f'{hour:02d}:{minute:02d}' for hour in range(16, 22) for minute in [0, 30]]

    if request.method == "POST":
        selected_time = request.POST.get("selected_time")
        if not selected_time:
            return JsonResponse({"success": False, "message": "No time selected."})

        try:
            # The selected time will come in format "Day Hour:Minute"
            day, time = selected_time.split()

            # Combine the day and time into a string like "2025-01-06 16:00"
            today = datetime.now()
            day_mapping = {
                "Saturday": 5,
                "Sunday": 6,
                "Monday": 0,
                "Tuesday": 1,
                "Wednesday": 2,
            }
            target_day = today + timedelta(days=(day_mapping[day] - today.weekday()) % 7)
            appointment_datetime_str = f"{target_day.date()} {time}"

            # Parse the appointment datetime string
            appointment_time = datetime.strptime(appointment_datetime_str, "%Y-%m-%d %H:%M")

            # Check if the user already has a reserved slot
            if Appointment.objects.filter(patient__user=user, doctor=doctor).exists():
                return JsonResponse({"success": False, "message": "You already have a slot reserved with this doctor."})

            # Check if the slot is already reserved by someone else
            if Appointment.objects.filter(doctor=doctor, date_time=appointment_time).exists():
                return JsonResponse({"success": False, "message": "This slot is already reserved."})

            if Appointment.objects.filter(patient__user=user, date_time=appointment_time).exists():
                return JsonResponse({"success": False, "message": "You cannot reserve appointments with two doctors at the same time."})

            # Create the appointment if all validations pass
            patient = Patient.objects.get(user=user)
            Appointment.objects.create(doctor=doctor, patient=patient, date_time=appointment_time, status="Confirmed")

            return JsonResponse({
                "success": True,
                "message": f"{user.username}, you reserved {time} on {day} with Dr. {doctor.name}.",
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    appointments = Appointment.objects.filter(doctor=doctor)
    slot_table = []

    for day in days_of_week:
        row = {"day": day, "slots": []}
        for time in time_slots:
            is_reserved = False
            is_reserved_by_user = False

            for appointment in appointments:
                appointment_day = appointment.date_time.strftime("%A")
                appointment_time = appointment.date_time.strftime("%H:%M")
                if appointment_day == day and appointment_time == time:
                    is_reserved = True
                    if appointment.patient.user == user:
                        is_reserved_by_user = True
                    break

            row["slots"].append({
                "time": time,
                "is_reserved": is_reserved,
                "is_reserved_by_user": is_reserved_by_user,
            })
        slot_table.append(row)

    return render(request, 'booking/doctor_details.html', {
        'doctor': doctor,
        'slot_table': slot_table,
    })



@api_view(['GET'])
def doctor_list(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    doctor_id = request.data.get('doctor_id')
    selected_time = request.data.get('selected_time')

    # Check if the doctor exists
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Check if the patient already has an appointment at the selected time
    if Appointment.objects.filter(patient=request.user.patient, date_time=selected_time).exists():
        return Response({'error': 'You already have an appointment at this time.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the selected time slot is already booked for this doctor
    if Appointment.objects.filter(doctor=doctor, date_time=selected_time).exists():
        return Response({'error': 'Slot already booked'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the appointment if no conflicts
    appointment = Appointment.objects.create(
        patient=request.user.patient,
        doctor=doctor,
        date_time=selected_time,
        status='Pending'
    )

    # Create a notification for the patient
    Notification.objects.create(
        user=request.user,
        message=f'Your appointment with Dr. {doctor.name} on {selected_time} is confirmed.'
    )

    return Response({'message': 'Appointment booked successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_review(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(doctor=doctor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_doctors(request):
    query = request.query_params.get('q', '')
    if not query:
        doctors = Doctor.objects.all()
    else:
        doctors = Doctor.objects.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query)
        )
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


def logout_view(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_slots(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    available_slots = doctor.get_available_slots()
    slots_data = []
    for day, slots in available_slots.items():
        for slot in slots:
            slots_data.append(slot.isoformat())
    return Response({"available_slots": slots_data})
