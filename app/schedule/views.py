import calendar

__author__ = 'ventsi'
from django.shortcuts import render
from app.models import Doctor

def doctor_shedule(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    return render(request, "schedule/doctor.html", { "doctor": doctor })