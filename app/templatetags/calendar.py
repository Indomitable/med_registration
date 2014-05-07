import datetime

__author__ = 'ventsi'
import calendar
from django import template

register = template.Library()
month_names = ['Януари', 'Февруари', 'Март', 'Април', 'Май', 'Юни', 'Юли', 'Август', 'Септември', 'Октомври',
               'Ноември', 'Декември']

week_day_names = ['пон', 'вт', 'ср', 'чет', 'пет', 'съб', 'нед']
days_of_week = 7

def close_month(body, current_date, weekcells):
    body += '<td colspan="{0}"></td>'.format(days_of_week - current_date.weekday())
    body += '</tr>'
    body += '<tr class="month"><td colspan="7">{0}</td></tr>'.format(month_names[current_date.month - 1])
    body += '<tr>'
    body += '<td colspan="{0}"></td>'.format(current_date.weekday())
    return body, current_date.month


@register.simple_tag()
def cal_html(number_days):
    header = '<table class="calendar"><thead><tr><th>' + '</th><th>'.join(week_day_names) + '</th></tr></thead><tbody>'
    footer = '</tbody></table>'

    today = datetime.date.today()
    month = today.month
    counter = 0

    weekcells = ['<td></td>', '<td></td>', '<td></td>', '<td></td>', '<td></td>', '<td></td>', '<td></td>']
    body = '<tr class="month"><td colspan="7">{0}</td></tr>'.format(month_names[today.month - 1])

    body += '<tr>'
    body += ''.join(weekcells[:today.weekday()])

    for i in range(today.weekday(), days_of_week):
        current_date = today + datetime.timedelta(days=counter)
        if current_date.month != month:
            body, month = close_month(body, current_date, weekcells)
        body += '<td class="day">{0}</td>'.format(current_date.day)
        counter += 1
    body += '</tr>'

    if number_days > counter:
        body += '<tr>'
        for i in range(0, number_days - counter):
            current_date = today + datetime.timedelta(days=i + counter)
            if current_date.month != month:
                body, month = close_month(body, current_date, weekcells)

            body += '<td class="day">{0}</td>'.format(current_date.day)
            if current_date.weekday() == 6:
                body += '</tr><tr>'

    return header + body + footer