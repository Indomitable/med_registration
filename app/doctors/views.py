__author__ = 'ventsi'
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from app.models import Doctor, Title


def doctors(request):
    data = Doctor.objects.all()
    return render(request, "doctors/list.html", {
        "doctors": data
    })


class AddDoctor(View):

    def get(self, request):
        return render(request, "doctors/add.html", {
            "titles": Title.objects.all()
        })

    def post(self, request):
        titlePk = request.POST.get("Title", "")
        firstName = request.POST.get('FirstName', '')
        lastName = request.POST.get('LastName', '')
        default_time_exam = request.POST.get('DefaultExampTime', 20)
        #Make some checks
        title = Title.objects.get(pk=titlePk)
        doctor = Doctor(title=title, first_name=firstName, last_name=lastName, default_exam_time=default_time_exam)
        doctor.save()
        return redirect(doctors)