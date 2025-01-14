from django.urls import path
from . import views

urlpatterns = [
    # Frontend pages
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.user_registration, name='register'),
    path('doctor/<int:doctor_id>/', views.doctor_details, name='doctor_details'),


    # API endpoints
    path('api/doctors/<int:doctor_id>/available_slots/', views.get_available_slots, name='get_available_slots'),
    path('doctor/<int:doctor_id>/', views.doctor_details, name='doctor_details'),
    path('api/doctors/', views.doctor_list, name='doctor_list'),
    path('api/doctors/<int:doctor_id>/review/', views.submit_review, name='submit_review'),
    path('api/appointments/', views.book_appointment, name='book_appointment'),
    path('api/appointments/list/', views.appointment_list, name='appointment_list'),
    path('api/doctors/search/', views.search_doctors, name='search_doctors'),

]
