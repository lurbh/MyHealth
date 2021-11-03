from django.shortcuts import render
from users.models import Patient, Doctor
from users.forms import *
from django.shortcuts import redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from .forms import *
from clinicadmin.models import *
from general.models import *
from general.forms import *
from datetime import date, datetime, timedelta, time
from django.db.models import Avg
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from icalendar import Calendar, Event
import tempfile, os
from django.contrib.auth.decorators import user_passes_test

def usertype_check(user):
    if user.is_authenticated:
        return user.is_patient
    else:
        return False

# Create your views here.
@user_passes_test(usertype_check)
def AccountView(request):
    patient = get_object_or_404(Patient, user_account_id=request.user.id)
    if request.method == 'POST':
      subform = SubscribeForm(request.POST)
      if subform.is_valid():
        email = subform.cleaned_data['email']
        sub = Subscriber.objects.create(email=email)
        sub.save()
        subform = SubscribeForm()
    else:
        subform = SubscribeForm()
    return render(request, "patient/account.html", {'patient':patient, 'subform': subform})

@user_passes_test(usertype_check)
def BookAppointmentView(request):
    patient = get_object_or_404(Patient, user_account_id=request.user.id)
    tz = timezone.get_current_timezone()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        subform = SubscribeForm(request.POST)
        if subform.is_valid():
          email = subform.cleaned_data['email']
          sub = Subscriber.objects.create(email=email)
          sub.save()
          subform = SubscribeForm()
        if form.is_valid():
            day = int(request.POST['appt-day'])
            month = int(request.POST['appt-month'])
            year = int(request.POST['appt-year'])
            hour = int(request.POST['appt-hour'])
            min = int(request.POST['appt-min'])
            sdate = date(year, month, day)
            stime = time(hour, min)
            clinicid = form.cleaned_data['clinicid']
            sdatetime = timezone.make_aware(datetime.combine(sdate, stime), tz, True)
            slot = Slot.objects.filter(clinicid=clinicid, occupied=False,datetimestart=sdatetime).first()
            if not slot:
              messages.error(request, 'No Slot available for that date and time')
            else:
              slot.occupied = True
              slot.save()
              appt = form.save()
              appt.slot = slot
              appt.name = appt.patientid.user_account.name
              appt.date = slot.datetimestart.date()
              appt.save()
              return redirect('appointments')
    else:
        form = AppointmentForm(initial={'patientid': patient.user_account.id})
        subform = SubscribeForm()
    return render(request, "patient/bookappointment.html", {'form':form, 'hour' : range(8 , 23), 'min' : range(0 , 60),
    'day' : range(1 , 32), 'month' : range(1 , 13), 'year' : range(2021 , 2026), 'subform': subform})

@user_passes_test(usertype_check)
def EditAccountView(request):
    patient = get_object_or_404(Patient, user_account_id=request.user.id)
    account = patient.user_account
    if request.method == 'POST':
        form = PatientChangeForm(request.POST, instance=account)
        subform = SubscribeForm(request.POST)
        if subform.is_valid():
          email = subform.cleaned_data['email']
          sub = Subscriber.objects.create(email=email)
          sub.save()
          subform = SubscribeForm()
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        name = patient.user_account.name
        username = patient.user_account.username
        phone = patient.phone
        email = patient.user_account.email
        form = PatientChangeForm(initial={'name': name, 'username': username, 'phone': phone, 'email':email })
        subform = SubscribeForm()
    return render(request, "patient/editaccount.html", {'form':form, 'subform': subform})

@user_passes_test(usertype_check)
def EditAppointmentView(request,id):
    patient = get_object_or_404(Patient, user_account_id=request.user.id)
    appt = get_object_or_404(Appointment, id=id)
    tz = timezone.get_current_timezone()
    clinicid = appt.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    minute = int(60 / clinic.apptinterval)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appt)
        subform = SubscribeForm(request.POST)
        if subform.is_valid():
          email = subform.cleaned_data['email']
          sub = Subscriber.objects.create(email=email)
          sub.save()
          subform = SubscribeForm()
        if form.is_valid():
            day = int(request.POST['appt-day'])
            month = int(request.POST['appt-month'])
            year = int(request.POST['appt-year'])
            hour = int(request.POST['appt-hour'])
            min = int(request.POST['appt-min'])
            sdate = date(year, month, day)
            stime = time(hour, min)
            clinicid = form.cleaned_data['clinicid']
            sdatetime = timezone.make_aware(datetime.combine(sdate, stime), tz, True)
            slot = Slot.objects.filter(clinicid=clinicid, occupied=False,datetime=sdatetime).first()
            if slot != appt.slot:
              appt.slot.occupied = False
              appt.slot.save()
            if not slot:
              messages.error(request, 'No Slot available for that date and time')
            else:
              slot.occupied = True
              slot.save()
              appt = form.save()
              appt.slot = slot
              appt.name = appt.patientid.user_account.name
              appt.date = slot.datetimestart.date()
              appt.save()
              return redirect('appointments')
    else:
        initialdetails = {
          'clinicid': appt.clinicid,
          'patientid': appt.patientid,
          'type': appt.type,
          'doctorid': appt.doctorid,
          'room': appt.room,
        }
        slotdetails = {
          'day': int(appt.slot.datetimestart.day),
          'month': int(appt.slot.datetimestart.month),
          'year': int(appt.slot.datetimestart.year),
          'hour': int(appt.slot.datetimestart.hour)+8,
          'min': int(appt.slot.datetimestart.minute),
        }
        form = AppointmentForm(initial=initialdetails)
        subform = SubscribeForm()
        form.fields["doctorid"].queryset = Doctor.objects.filter(clinicid=clinicid)
    return render(request, "patient/editappointment.html", {'form':form, 'hour' : range(8 , 23), 'min': minute, 'range' : range(0 , clinic.apptinterval),
    'day' : range(1 , 32), 'month' : range(1 , 13), 'year' : range(2021 , 2026), 'slotdetails' : slotdetails, 'subform': subform})

@user_passes_test(usertype_check)
def PastAppointmentsView(request):
    today = datetime.today().date()
    appointments = Appointment.objects.filter(patientid=request.user.id,date__lt=today).order_by('date')
    if request.method == 'POST':
      subform = SubscribeForm(request.POST)
      if subform.is_valid():
        email = subform.cleaned_data['email']
        sub = Subscriber.objects.create(email=email)
        sub.save()
        subform = SubscribeForm()
    else:
        subform = SubscribeForm()
    return render(request, "patient/pastappointments.html", {'appointments':appointments, 'subform': subform})

@user_passes_test(usertype_check)
def RateAppointmentView(request,id):
    appt = get_object_or_404(Appointment, id=id)
    clinic = get_object_or_404(Clinic, id=appt.clinicid.id)
    appointments = Appointment.objects.filter(clinicid=appt.clinicid)
    if request.method == 'POST':
        form = AppointmentRateForm(request.POST, instance=appt)
        subform = SubscribeForm(request.POST)
        if subform.is_valid():
          email = subform.cleaned_data['email']
          sub = Subscriber.objects.create(email=email)
          sub.save()
          subform = SubscribeForm()
        if form.is_valid():
            form.save()
            appointments = appointments.filter(rating__gt=0)
            avrrating = appointments.aggregate(Avg('rating'))
            clinic.rating = round(avrrating['rating__avg'],2)
            return redirect('pastappointments')
    else:
        form = AppointmentRateForm()
        subform = SubscribeForm()
    return render(request, "patient/rateappointment.html", {'form':form, 'appt':appt, 'subform': subform})

@user_passes_test(usertype_check)
def AppointmentsView(request):
    today = datetime.today().date()
    appointments = Appointment.objects.filter(patientid=request.user.id,date__gte=today).order_by('date')
    if request.method == 'POST':
      subform = SubscribeForm(request.POST)
      if subform.is_valid():
        email = subform.cleaned_data['email']
        sub = Subscriber.objects.create(email=email)
        sub.save()
        subform = SubscribeForm()
    else:
        subform = SubscribeForm()
    return render(request, "patient/viewappointments.html", {'appointments':appointments, 'subform': subform})
  
@user_passes_test(usertype_check)  
def ChangePasswordView(request):
    patient = get_object_or_404(Patient, user_account_id=request.user.id)
    account = patient.user_account
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        subform = SubscribeForm(request.POST)
        if subform.is_valid():
          email = subform.cleaned_data['email']
          sub = Subscriber.objects.create(email=email)
          sub.save()
          subform = SubscribeForm()
        if form.is_valid():
            oldpass = form.cleaned_data['oldpassword']
            if account.check_password(oldpass):
              pass1 = form.cleaned_data['password']
              pass2 = form.cleaned_data['password1']
              if pass1 == pass2:
                  account.set_password(pass1)
                  account.save()
                  update_session_auth_hash(request, account)  
                  return redirect('account')
              else:
                  messages.error(request, 'New Passwords do not match')
            else:
                messages.error(request, 'Password do not match existing password')
    else:
        form = ChangePasswordForm()
        subform = SubscribeForm()
    return render(request, "patient/changepassword.html", {'form':form, 'subform': subform})

@user_passes_test(usertype_check)
def ConfirmAppointmentView(request,id):
    patient = get_object_or_404(Patient, user_account_id=request.user.id)
    account = patient.user_account
    appt = get_object_or_404(Appointment, id=id)
    plaintext = get_template('email/appointment.txt')
    html = get_template('email/appointment.html')
    appt.confirm = True
    appt.save()
    clinic = appt.clinicid
    date = ((appt.slot.datetimestart)+ timedelta(hours=8)).strftime('%d/%m/%Y')
    time = ((appt.slot.datetimestart)+ timedelta(hours=8)).strftime('%H:%M')
    subject = "Appointment for " + account.name + " on " + date + " at " + clinic.name
    details = ""
    if appt.doctorid is not None:
      details = appt.type.type + " Appointment with " + appt.doctorid.user_account.name
    else:
      details = appt.type.type + " Appointment"
    when = ((appt.slot.datetimestart)+ timedelta(hours=8)).strftime('%A, %B %d, %Y %H:%M')
    d = { 'name': account.name, 'appointment': details, 'when': when, 'where': clinic.address, 'room': appt.room.location }
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    event = Event()
    event.add('summary', subject)
    event.add('dtstart', appt.slot.datetimestart)
    event.add('dtend', appt.slot.datetimeend)
    event.add('dtstamp', datetime.now())
    event.add('description', details)
    event.add('location', clinic.address)
    cal.add_component(event)
    directory = tempfile.mkdtemp()
    file = os.path.join(directory, 'appointment.ics')
    f = open(file, 'wb')
    f.write(cal.to_ical())
    f.close()
    text_content = plaintext.render(d)
    html_content = html.render(d)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [account.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.attach_file(file)
    email.send()
    return redirect('appointments')

@user_passes_test(usertype_check)
def CancelAppointmentView(request,id):
    appt = get_object_or_404(Appointment, id=id)
    appt.slot.occupied = False
    appt.delete()
    return redirect('appointments')


def load_clinic_doctors(request):
    clinicid = request.GET.get('clinicid')
    doctors = Doctor.objects.filter(clinicid=clinicid)
    return render(request, 'patient/clinic_options_doctors.html', {'doctors': doctors})
    
def load_clinic_slots(request):
    clinicid = request.GET.get('clinicid')
    clinic = get_object_or_404(Clinic, id=clinicid)
    minute = 0
    if clinic.apptinterval != 0:
      minute = int(60 / clinic.apptinterval)
    return render(request, 'patient/clinic_options_slots.html', {'min': minute, 'range' : range(0 , clinic.apptinterval)})