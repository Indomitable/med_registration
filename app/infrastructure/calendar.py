import itertools
import datetime


class Day:
    def __init__(self, date, is_empty=False):
        self.is_empty = is_empty
        self.date = date

    def __str__(self):
        return self.date

    @staticmethod
    def empty():
        min_date = datetime.date.min
        return Day(min_date, is_empty=True)

    def to_dict(self):
        return dict({
            'date': '' if self.is_empty else self.date.__str__(),
            'on_work': False
        })

class Week:
    days_of_week = 7

    def __init__(self):
        self.days = []

    def to_dict(self):
        return list(d.to_dict() for d in self.days)


class Month:
    month_names = ['Януари', 'Февруари', 'Март', 'Април', 'Май', 'Юни', 'Юли', 'Август', 'Септември', 'Октомври',
                   'Ноември', 'Декември']

    def __init__(self, number):
        self.name = self.month_names[number]
        self.weeks = []

    def add_week(self, first_week, date, max_date):
        week = Week()
        if first_week or date.day == 1:
            week.days.extend(itertools.repeat(Day.empty(), date.weekday()))
        for i in range(date.weekday(), Week.days_of_week):
            current_date = date + datetime.timedelta(days=i - date.weekday())
            week.days.append(Day(date=current_date))
            if current_date == max_date or (current_date + datetime.timedelta(days=1)).day == 1:
                week.days.extend(itertools.repeat(Day.empty(), Week.days_of_week - current_date.weekday() - 1))
                self.weeks.append(week)
                return current_date
        self.weeks.append(week)
        return week.days[Week.days_of_week - 1].date

    def to_dict(self):
        return dict({
            'name': self.name,
            'weeks': list(w.to_dict() for w in self.weeks)
        })


class Calendar:

    def __init__(self):
        self.months = []

    def add_month(self, number):
        month = Month(number)
        self.months.append(month)
        return month

    def build_calendar(self, number_of_days, doctor_id):
        from_day = datetime.date.today()
        to_day = from_day + datetime.timedelta(days=number_of_days)
        current_date = from_day
        month = self.add_month(current_date.month)
        current_date = month.add_week(True, from_day, to_day) + datetime.timedelta(days=1)
        while current_date < to_day:
            if current_date.day == 1:
                month = self.add_month(current_date.month)
            current_date = month.add_week(False, current_date, to_day) + datetime.timedelta(days=1)

    def to_dict(self):
        return list(m.to_dict() for m in self.months)