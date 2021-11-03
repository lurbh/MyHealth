from django.shortcuts import render
from users.models import Doctor
from patient.models import *
from clinicadmin.utils import Calendar, DoctorCalendar
from clinicadmin.models import DoctorSchedule
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, get_object_or_404
from users.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import *
from django.utils import timezone
from datetime import date, datetime, timedelta, time
import calendar
import holidays

from django.contrib.auth.decorators import user_passes_test

def usertype_check(user):
    if user.is_authenticated:
        return user.is_doctor
    else:
        return False

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Create your views here.
@user_passes_test(usertype_check)
def OverviewView(request):
    today = datetime.today().date()
    week = [today + timedelta(days=i) for i in range(0 - today.weekday() - 1, 7 - today.weekday() - 1)]
    appointments = Appointment.objects.filter(doctorid=request.user.id)
    appointments = appointments.filter(date__gte=week[0],date__lte=week[-1])
    appointments = appointments.filter(date__gte=today).order_by('date')
    docschedule = get_object_or_404(DoctorSchedule,doctorid=request.user.id)
    sg_holidays = holidays.Singapore()
    tz = timezone.get_current_timezone()
    weekschedule = {}
    for day in week:
      if day in sg_holidays:
        if docschedule.phstart is not None:
          timestart = timezone.make_aware(datetime.combine(day, docschedule.phstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(day, docschedule.phend), tz, True).strftime("%H:%M")
          weekschedule[day] = timestart + "-" + timeend
        else:
          weekschedule[day] = "-- N/A --"
      elif day.isoweekday() >= 1 and day.isoweekday() <= 5:
        if docschedule.weekdaystart is not None:
          timestart = timezone.make_aware(datetime.combine(day, docschedule.weekdaystart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(day, docschedule.weekdayend), tz, True).strftime("%H:%M")
          weekschedule[day] = timestart + "-" + timeend
        else:
          weekschedule[day] = "-- N/A --"
      elif day.isoweekday() == 6:
        if docschedule.satstart is not None:
          timestart = timezone.make_aware(datetime.combine(day, docschedule.satstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(day, docschedule.satend), tz, True).strftime("%H:%M")
          weekschedule[day] = timestart + "-" + timeend
        else:
          weekschedule[day] = "-- N/A --"
      elif day.isoweekday() == 7:
        if docschedule.sunstart is not None:
          timestart = timezone.make_aware(datetime.combine(day, docschedule.sunstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(day, docschedule.sunend), tz, True).strftime("%H:%M")
          weekschedule[day] = timestart + "-" + timeend
        else:
          weekschedule[day] = "-- N/A --"
    return render(request, "doctor/overview.html", {'weekschedule': weekschedule, 'appointments': appointments})

@user_passes_test(usertype_check)
def AppointmentsView(request):
    today = datetime.today().date()
    appointments = Appointment.objects.filter(doctorid=request.user.id,date__gte=today).order_by('date')
    datesubmit = request.GET.get('inputdate', False)
    if datesubmit != False:
      datesubmit = datetime.strptime(datesubmit, "%Y-%m-%d")
      appointments = appointments.filter(date=datesubmit.date())
    return render(request, "doctor/appointments.html", {'appointments': appointments})

@user_passes_test(usertype_check)
def PastAppointmentsView(request):
    today = datetime.today().date()
    appointments = Appointment.objects.filter(doctorid=request.user.id,date__lt=today).order_by('date')
    name = request.GET.get('inputname', False)
    if name != False:
      appointments = appointments.filter(name__icontains=name)
    return render(request, "doctor/pastappointments.html", {'appointments': appointments, 'name': name})

@user_passes_test(usertype_check)
def ScheduleView(request):
    doc = get_object_or_404(Doctor, user_account_id=request.user.id)
    account = doc.user_account
    context = {}
    d = get_date(request.GET.get('month', None))
    cal = DoctorCalendar(d.year, d.month,account.id)
    html_cal = cal.formatmonth(withyear=True)
    tz = timezone.get_current_timezone()
    now = date.today()
    start_date = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
    end_date = start_date.replace(day = calendar.monthrange(start_date.year, start_date.month)[1]) + timedelta(days=1)
    docschedule = get_object_or_404(DoctorSchedule,doctorid=account.id)
    sg_holidays = holidays.Singapore()
    scheduledict = {}
    for single_date in daterange(start_date, end_date):
      if single_date in sg_holidays:
        if docschedule.phstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.phstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.phend), tz, True).strftime("%H:%M")
          scheduledict[single_date] = timestart + "-" + timeend
        else:
          scheduledict[single_date] = "-- N/A --"
      elif single_date.isoweekday() >= 1 and single_date.isoweekday() <= 5:
        if docschedule.weekdaystart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.weekdaystart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.weekdayend), tz, True).strftime("%H:%M")
          scheduledict[single_date] = timestart + "-" + timeend
        else:
          scheduledict[single_date] = "-- N/A --"
      elif single_date.isoweekday() == 6:
        if docschedule.satstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.satstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.satend), tz, True).strftime("%H:%M")
          scheduledict[single_date] = timestart + "-" + timeend
        else:
          scheduledict[single_date] = "-- N/A --"
      elif single_date.isoweekday() == 7:
        if docschedule.sunstart is not None:
          timestart = timezone.make_aware(datetime.combine(single_date, docschedule.sunstart), tz, True).strftime("%H:%M")
          timeend = timezone.make_aware(datetime.combine(single_date, docschedule.sunend), tz, True).strftime("%H:%M")
          scheduledict[single_date] = timestart + "-" + timeend
        else:
          scheduledict[single_date] = "-- N/A --"
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)
    context['scheduledict'] = scheduledict
    return render(request, "doctor/viewschedule.html", context)

@user_passes_test(usertype_check)
def AccountView(request):
    doctor = get_object_or_404(Doctor, user_account_id=request.user.id)
    return render(request, "doctor/account.html", {'doctor': doctor})

@user_passes_test(usertype_check)
def ChangePasswordView(request):
    doc = get_object_or_404(Doctor, user_account_id=request.user.id)
    account = doc.user_account
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            oldpass = form.cleaned_data['oldpassword']
            if account.check_password(oldpass):
              pass1 = form.cleaned_data['password']
              pass2 = form.cleaned_data['password1']
              if pass1 == pass2:
                  account.set_password(pass1)
                  account.save()
                  update_session_auth_hash(request, account)  
                  return redirect('docaccount')
              else:
                  messages.error(request, 'New Passwords do not match')
            else:
                messages.error(request, 'Password do not match existing password')
    else:
        form = ChangePasswordForm()
    return render(request, "doctor/changepassword.html", {'form': form})

@user_passes_test(usertype_check)
def EditAccountView(request):
    doctor = get_object_or_404(Doctor, user_account_id=request.user.id)
    account = doctor.user_account
    if request.method == 'POST':
        form = DoctorChangeForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('docaccount')
    else:
        docname = doctor.user_account.name
        docusername = doctor.user_account.username
        docspecial = doctor.specialty.all
        form = DoctorChangeForm(initial={'name': docname, 'username': docusername, 'specialty': docspecial })
    return render(request, "doctor/editaccount.html", {'form': form})

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#def SetScheduleView(request):
#    return render(request, "doctor/setschecule.html")

#def EditScheduleView(request):
#    return render(request, "doctor/editschedule.html")

#def BlockscheduleView(request):
#    return render(request, "doctor/blockoutdates.html")