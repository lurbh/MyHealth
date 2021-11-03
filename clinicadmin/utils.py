from datetime import datetime, timedelta, time, date
from calendar import HTMLCalendar
from .models import PublicHoliday, DoctorSchedule
from patient.models import Appointment
from systemadmin.models import Clinic
from users.models import Doctor
from django.shortcuts import get_object_or_404
from django.utils import timezone
import calendar

class Calendar(HTMLCalendar):
  def __init__(self, year=None, month=None, *args):
    self.year = year
    self.month = month
    self.clinicid = args[0]
    super(Calendar, self).__init__(calendar.SUNDAY)

  # formats a day as a td
  # filter events by day
  def formatday(self, day, events):
    events_per_day = events.filter(date__day=day)
    clinic = get_object_or_404(Clinic, id=self.clinicid)
    doctors = Doctor.objects.filter(clinicid=self.clinicid)
    tz = timezone.get_current_timezone()
    d = ''
    for event in events_per_day:
      d += f'<li> {event.name} </li>'
    
    
    
    if day != 0:
      single_date = date(self.year, self.month, day)
      if len(events_per_day) != 0:
        if clinic.openinghours.phstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.phstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.phend), tz, True).strftime("%H:%M")
          d += f'<li> Opening Hours: {timestart}-{timeend} </li>'
      elif single_date.isoweekday() >= 1 and single_date.isoweekday() <= 5:
        if clinic.openinghours.weekdaystart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.weekdaystart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.weekdayend), tz, True).strftime("%H:%M")
          d += f'<li> Opening Hours: {timestart}-{timeend} </li>'
      elif single_date.isoweekday() == 6:
        if clinic.openinghours.satstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.satstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.satend), tz, True).strftime("%H:%M")
          d += f'<li> Opening Hours: {timestart}-{timeend} </li>'
      elif single_date.isoweekday() == 7:
        if clinic.openinghours.sunstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.sunstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.sunend), tz, True).strftime("%H:%M")
          d += f'<li> Opening Hours: {timestart}-{timeend} </li>'
    
      for doc in doctors:
        docschedule = DoctorSchedule.objects.filter(doctorid=doc.user_account.id).first()
        if docschedule is not None:
          if len(events_per_day) != 0:
            if docschedule.phstart is not None:
              timestart = timezone.make_aware(datetime.combine(single_date, docschedule.phstart), tz, True).strftime("%H:%M")
              timeend = timezone.make_aware(datetime.combine(single_date, docschedule.phend), tz, True).strftime("%H:%M")
              d += f'<li> {doc.user_account.name}: {timestart}-{timeend} </li>'
          elif single_date.isoweekday() >= 1 and single_date.isoweekday() <= 5:
            if docschedule.weekdaystart is not None:
              timestart = timezone.make_aware(datetime.combine(single_date, docschedule.weekdaystart), tz, True).strftime("%H:%M")
              timeend = timezone.make_aware(datetime.combine(single_date, docschedule.weekdayend), tz, True).strftime("%H:%M")
              d += f'<li> {doc.user_account.name}: {timestart}-{timeend} </li>'
          elif single_date.isoweekday() == 6:
            if docschedule.satstart is not None:
              timestart = timezone.make_aware(datetime.combine(single_date, docschedule.satstart), tz, True).strftime("%H:%M")
              timeend = timezone.make_aware(datetime.combine(single_date, docschedule.satend), tz, True).strftime("%H:%M")
              d += f'<li> {doc.user_account.name}: {timestart}-{timeend} </li>'
          elif single_date.isoweekday() == 7:
            if docschedule.sunstart is not None:
              timestart = timezone.make_aware(datetime.combine(single_date, docschedule.sunstart), tz, True).strftime("%H:%M")
              timeend = timezone.make_aware(datetime.combine(single_date, docschedule.sunend), tz, True).strftime("%H:%M")
              d += f'<li> {doc.user_account.name}: {timestart}-{timeend} </li>'
    
    
    
    if day != 0:
      single_date = date(self.year, self.month, day)
      today = datetime.now()
      for event in events_per_day:
        return f"<td class='publicholiday'><span class='date'>{day}</span><ul> {d} </ul></td>"
      if today.date() == single_date:
        return f"<td class='today'><span class='date'>{day}</span><ul> {d} </ul></td>"
      return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
    return '<td></td>'

	# formats a week as a tr 
  def formatweek(self, theweek, events):
    week = ''
    for d, weekday in theweek:
      week += self.formatday(d, events)
    return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
  def formatmonth(self, withyear=True):
    events = PublicHoliday.objects.filter(date__year=self.year, date__month=self.month)

    cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
    cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
    cal += f'{self.formatweekheader()}\n'
    for week in self.monthdays2calendar(self.year, self.month):
      cal += f'{self.formatweek(week, events)}\n'
    cal += f'</table>\n'
    return cal

class DoctorCalendar(HTMLCalendar):
  def __init__(self, year=None, month=None, *args):
    self.year = year
    self.month = month
    self.doctorid = args
    super(DoctorCalendar, self).__init__(calendar.SUNDAY)

  # formats a day as a td
  # filter events by day
  def formatday(self, day, events, apptevents):
    events_per_day = events.filter(date__day=day)
    apptevents_per_day = apptevents.filter(date__day=day)
    docschedule = get_object_or_404(DoctorSchedule,doctorid=self.doctorid)
    tz = timezone.get_current_timezone()
    d = ''
    for event in events_per_day:
      d += f'<li> {event.name} </li>'
    
    if day != 0:
      single_date = date(self.year, self.month, day)
      if len(events_per_day) != 0:
        if docschedule.phstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.phstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.phend), tz, True).strftime("%H:%M")
          d += f'<li> Appointment Hours: {timestart}-{timeend} </li>'
      elif single_date.isoweekday() >= 1 and single_date.isoweekday() <= 5:
        if docschedule.weekdaystart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.weekdaystart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.weekdayend), tz, True).strftime("%H:%M")
          d += f'<li> Appointment Hours: {timestart}-{timeend} </li>'
      elif single_date.isoweekday() == 6:
        if docschedule.satstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.satstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.satend), tz, True).strftime("%H:%M")
          d += f'<li> Appointment Hours: {timestart}-{timeend} </li>'
      elif single_date.isoweekday() == 7:
        if docschedule.sunstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.sunstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.sunend), tz, True).strftime("%H:%M")
          d += f'<li> Appointment Hours: {timestart}-{timeend} </li>'
    
    for appt in apptevents_per_day:
      timestart = (appt.slot.datetimestart + timedelta(hours=8)).strftime("%H:%M")
      timeend = (appt.slot.datetimeend + timedelta(hours=8)).strftime("%H:%M")
      d += f'<li> {appt.name} ({timestart}-{timeend})</li>'
    
    
    
    if day != 0:
      single_date = date(self.year, self.month, day)
      today = datetime.now()
      if today.date() == single_date:
        return f"<td class='today'><span class='date'>{day}</span><ul> {d} </ul></td>"
      for event in events_per_day:
        return f"<td class='publicholiday'><span class='date'>{day}</span><ul> {d} </ul></td>"
      return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
    return '<td></td>'

	# formats a week as a tr 
  def formatweek(self, theweek, events, apptevents):
    week = ''
    for d, weekday in theweek:
      week += self.formatday(d, events, apptevents)
    return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
  def formatmonth(self, withyear=True):
    events = PublicHoliday.objects.filter(date__year=self.year, date__month=self.month)
    apptevents = Appointment.objects.filter(date__year=self.year, date__month=self.month)
    
    cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
    cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
    cal += f'{self.formatweekheader()}\n'
    for week in self.monthdays2calendar(self.year, self.month):
      cal += f'{self.formatweek(week, events, apptevents)}\n'
    cal += f'</table>\n'
    return cal