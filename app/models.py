from django.db import models


class Title(models.Model):
    abr = models.CharField(max_length=10)
    name = models.CharField(max_length=100)


class Specialty(models.Model):
    name = models.CharField(max_length=100)
    doctors = models.ManyToManyField("Doctor")


class Doctor(models.Model):
    title = models.ForeignKey(Title)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    default_exam_time = models.IntegerField(default=20)
    specialities = models.ManyToManyField(Specialty)


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor)
    date = models.DateField()
    note = models.CharField(max_length=1000)


class ScheduleDate(models.Model):
    schedule = models.ForeignKey(Schedule)
    from_time = models.TimeField()
    to_time = models.TimeField()
    nzok = models.BooleanField(default=False)

    def to_dict(self):
        from_time = self.from_time.hour + self.from_time.minute / 60
        to_time = self.to_time.hour + self.to_time.minute / 60
        return dict({
            'from': from_time,
            'to': to_time,
            'nzok': self.nzok
        })


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ident_number = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=250)


class PayType(models.Model):
    type = models.CharField(max_length=100)


class Reservation(models.Model):
    shedule = models.ForeignKey(Schedule)
    patient = models.ForeignKey(Patient)
    payType = models.ForeignKey(PayType)