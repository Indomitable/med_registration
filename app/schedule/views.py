import json
import datetime
import math
from django.http.response import HttpResponse
from django.shortcuts import render
from app.infrastructure.calendar import Calendar
from app.infrastructure.helpers import json_response
from app.models import Doctor, Schedule, ScheduleDate


def doctor_shedule(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    return render(request, "schedule/doctor.html", {"doctor": doctor})


def get_calendar(request):
    assert request.GET.get('days') != '', "Days are required"
    assert request.GET.get('doctor') != '', "Doctor ID is required"
    days = int(request.GET.get('days'))
    doctor = int(request.GET.get('doctor'))
    calendar = Calendar()
    calendar.build_calendar(int(days), int(doctor))
    return json_response(calendar.to_dict())


def set_work_hours(request):
    data = json.loads(request.body.decode(request.encoding))
    for date_str in data['days']:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        existing_schedule = Schedule.objects.filter(doctor_id=data['doctor'], date=date)
        if len(existing_schedule) > 0:
            schedule = existing_schedule[0]
            if len(data['note']) == 0 and len(data['intervals']) == 0:
                schedule.scheduledate_set.all().delete()
                schedule.delete()
                return HttpResponse("OK")

            schedule.note = data['note']
            schedule.save()
            schedule.scheduledate_set.all().delete()
        else:
            schedule = Schedule.objects.create(doctor_id=data['doctor'], date=date, note=data['note'])
        for interval in data['intervals']:
            from_time = datetime.datetime.strptime(str(math.floor(interval['interval'][0])) + ':' +
                                                   str(math.floor((interval['interval'][0] % 1) * 60)), '%H:%M').time()

            to_time = datetime.datetime.strptime(str(math.floor(interval['interval'][1])) + ':' +
                                                 str(math.floor((interval['interval'][1] % 1) * 60)), '%H:%M').time()

            nzok = interval['nzok']
            ScheduleDate.objects.create(schedule=schedule, from_time=from_time, to_time=to_time, nzok=nzok)
    return HttpResponse("OK")


def get_work_hours(request, pdate, pdoctor_id):
    date = datetime.datetime.strptime(pdate, '%Y-%m-%d').date()
    doctor = int(pdoctor_id)
    existing_schedules = Schedule.objects.filter(doctor_id=doctor, date=date)
    if len(existing_schedules) == 0:
        return json_response([])
    else:
        schedule = existing_schedules[0]
        schedules_as_dict = list(s.to_dict() for s in schedule.scheduledate_set.all())
        return json_response({
            'note': schedule.note,
            'hours': schedules_as_dict
        })