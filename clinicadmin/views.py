from django.shortcuts import render
from systemadmin.models import Clinic
from users.models import Doctor, ClinicAdmin, BaseUser, Patient
from django.shortcuts import redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from users.forms import *
from .models import *
from patient.models import Appointment
from patient.forms import AppointmentAdminForm
from django.contrib.auth import update_session_auth_hash
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar, DoctorCalendar
from django.utils import timezone
from general.models import *
from django.template.loader import get_template
from django.template import Context

from datetime import date, datetime, timedelta, time
import holidays
import calendar

from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.conf import settings

from django.contrib.auth.decorators import user_passes_test

def usertype_check(user):
    if user.is_authenticated:
        return user.is_clinicadmin
    else:
        return False

# Create your views here.
@user_passes_test(usertype_check)
def OverviewView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    return render(request, "clinicadmin/overview.html", {'clinic': clinic})

@user_passes_test(usertype_check)
def DoctorAccountsView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    doctors = Doctor.objects.filter(clinicid=clinicid)
    return render(request, "clinicadmin/doctoraccounts.html", {'doctors': doctors})

@user_passes_test(usertype_check)
def AddDoctorView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadmindocaccounts')
    else:
        form = DoctorForm(initial={'clinic': clinicid})
    return render(request, "clinicadmin/adddoctor.html", {'form': form})

@user_passes_test(usertype_check)
def RequestAccountView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    if request.method == 'POST':
        form = AdminRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadmindocaccounts')
    else:
        form = AdminRequestForm(initial={'clinicid': clinicid})
    return render(request, "clinicadmin/requestaccount.html", {'form': form})

@user_passes_test(usertype_check)
def AppointmentsView(request):
    today = datetime.today().date()
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    appointments = Appointment.objects.filter(clinicid=clinicid,date__gte=today).order_by('date')
    word = "Consultation"
    return render(request, "clinicadmin/appointments.html", {'appointments': appointments, 'word':word})

@user_passes_test(usertype_check)    
def AppointmentView(request,id):
    return render(request, "clinicadmin/appointment.html")

@user_passes_test(usertype_check)
def EducationView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    educationmats = EducationMaterial.objects.filter(clinicid=clinicid).order_by('id')
    return render(request, "clinicadmin/education.html", {'educationmats': educationmats})

@user_passes_test(usertype_check)
def PromotionView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    promsgs = PromotionalMessage.objects.filter(clinicid=clinicid).order_by('id')
    return render(request, "clinicadmin/promotion.html", {'promsgs': promsgs})

@user_passes_test(usertype_check)
def AccountView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    return render(request, "clinicadmin/account.html" , {'cadmin': cadmin})

@user_passes_test(usertype_check)
def AddAppointmentView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    slots = Slot.objects.filter(clinicid=clinicid, occupied=False)
    minute = int(60 / clinic.apptinterval)
    tz = timezone.get_current_timezone()
    if request.method == 'POST':
        form = AppointmentAdminForm(request.POST)
        if form.is_valid():
            day = int(request.POST['appt-day'])
            month = int(request.POST['appt-month'])
            year = int(request.POST['appt-year'])
            hour = int(request.POST['appt-hour'])
            min = int(request.POST['appt-min'])
            sdate = date(year, month, day)
            stime = time(hour, min)
            sdatetime = timezone.make_aware(datetime.combine(sdate, stime), tz, True)
            slot = slots.filter(datetimestart=sdatetime).first()
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
              return redirect('cadminappointments')
    else:
        form = AppointmentAdminForm(initial={'clinicid': clinicid})
        form.fields["doctorid"].queryset = Doctor.objects.filter(clinicid=clinicid)
        form.fields["room"].queryset = Room.objects.filter(clinicid=clinicid)
    return render(request, "clinicadmin/addappointment.html", {'form': form, 'min': minute, 'range' : range(0 , clinic.apptinterval), 'hour' : range(8 , 23),
    'day' : range(1 , 32), 'month' : range(1 , 13), 'year' : range(2021 , 2026)})

@user_passes_test(usertype_check)
def ChangePasswordView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    account = cadmin.user_account
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
                  return redirect('cadminaaccount')
              else:
                  messages.error(request, 'New Passwords do not match')
            else:
                messages.error(request, 'Password do not match existing password')
    else:
        form = ChangePasswordForm()
    return render(request, "clinicadmin/changepassword.html", {'form': form})

@user_passes_test(usertype_check)
def EditAccountView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    account = cadmin.user_account
    if request.method == 'POST':
        form = ClinicAdminChangeForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('cadminaaccount')
    else:
        caname = cadmin.user_account.name
        causername = cadmin.user_account.username
        form = ClinicAdminChangeForm(initial={'name': caname, 'username': causername })
    return render(request, "clinicadmin/editaccount.html", {'form': form})

@user_passes_test(usertype_check)
def EditDoctorView(request,id):
    doctor = get_object_or_404(Doctor, user_account_id=id)
    account = doctor.user_account
    fkey = doctor.clinicid.id
    clinic = get_object_or_404(Clinic, id=fkey)
    if request.method == 'POST':
        form = DoctorChangeForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('cadmindocaccounts')
    else:
        docname = doctor.user_account.name
        docusername = doctor.user_account.username
        docspecial = doctor.specialty.all
        form = DoctorChangeForm(initial={'name': docname, 'username': docusername, 'specialty': docspecial })
    return render(request, "clinicadmin/editdoctor.html", {'form': form})

@user_passes_test(usertype_check)
def EditAppointmentView(request,id):
    appt = get_object_or_404(Appointment, id=id)
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    slots = Slot.objects.filter(clinicid=clinicid, occupied=False)
    min = int(60 / clinic.apptinterval)
    tz = timezone.get_current_timezone()
    slotdetails = {
      'day': int(appt.slot.datetimestart.day),
      'month': int(appt.slot.datetimestart.month),
      'year': int(appt.slot.datetimestart.year),
      'hour': int(appt.slot.datetimestart.hour)+8,
      'min': int(appt.slot.datetimestart.minute / min),
    }
    if request.method == 'POST':
        form = AppointmentAdminForm(request.POST, instance=appt)
        if form.is_valid():
            day = int(request.POST['appt-day'])
            month = int(request.POST['appt-month'])
            year = int(request.POST['appt-year'])
            hour = int(request.POST['appt-hour'])
            min = int(request.POST['appt-min'])
            sdate = date(year, month, day)
            stime = time(hour, min)
            sdatetime = timezone.make_aware(datetime.combine(sdate, stime), tz, True)
            slot = slots.filter(datetimestart=sdatetime).first()
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
              if appt.room is not None:
                appt.canconfirm = True
                plaintext = get_template('email/confirm.txt')
                html = get_template('email/confirm.html')
                patient = get_object_or_404(Patient, user_account_id=appt.patientid.user_account.id)
                account = patient.user_account
                datemail = ((appt.slot.datetimestart)+ timedelta(hours=8)).strftime('%d/%m/%Y')
                subject = "Appointment for " + account.name + " on " + datemail + " at " + clinic.name
                details = ""
                if appt.doctorid is not None:
                  details = appt.type.type + " Appointment with " + appt.doctorid.user_account.name
                else:
                  details = appt.type.type + " Appointment"
                when = ((appt.slot.datetimestart)+ timedelta(hours=8)).strftime('%A, %B %d, %Y %H:%M')
                d = { 'name': appt.patientid.user_account.name, 'appointment': details, 'when': when, 'where': clinic.address, 'room': appt.room.location }
                text_content = plaintext.render(d)
                html_content = html.render(d)
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [account.email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
              appt.save()
              return redirect('cadminappointments')
    else:
        initialdetails = {
          'clinicid': appt.clinicid,
          'patientid': appt.patientid,
          'type': appt.type,
          'doctorid': appt.doctorid,
          'room': appt.room,
        }
        form = AppointmentAdminForm(initial=initialdetails)
        form.fields["doctorid"].queryset = Doctor.objects.filter(clinicid=clinicid)
        form.fields["room"].queryset = Room.objects.filter(clinicid=clinicid)
    return render(request, "clinicadmin/editappointment.html", {'form': form, 'min': min, 'range' : range(0 , clinic.apptinterval), 'slotdetails' : slotdetails, 
    'hour' : range(8 , 23), 'day' : range(1 , 32), 'month' : range(1 , 13), 'year' : range(2021 , 2026)})

@user_passes_test(usertype_check)
def EditOverviewView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    if request.method == 'POST':
        clinicform = ClinicOverviewForm(request.POST, request.FILES, instance=clinic)
        hoursform = OpeningHoursForm(request.POST, instance=clinic.openinghours)
        if hoursform.is_valid() and clinicform.is_valid():
            if request.method == 'POST':
              hoursform.save()
              clinicform.save()
              return redirect('cadminoverview')
    else:
        clinicform = ClinicOverviewForm(initial={'name': clinic.name, 'address': clinic.address, 'phone': clinic.phone, 'email': clinic.email, 
        'apptinterval': clinic.apptinterval, 'doctorinterval': clinic.doctorinterval, 'image': clinic.image })
        hoursform = OpeningHoursForm(initial={'weekdaystart': clinic.openinghours.weekdaystart, 'weekdayend': clinic.openinghours.weekdayend, 'satstart': clinic.openinghours.satstart, 'satend': clinic.openinghours.satend, 
        'sunstart': clinic.openinghours.sunstart, 'sunend': clinic.openinghours.sunend, 'phstart': clinic.openinghours.phstart, 'phend': clinic.openinghours.phend })
    return render(request, "clinicadmin/editoverview.html", {'clinicform': clinicform, 'hoursform': hoursform })

@user_passes_test(usertype_check)
def UploadEducationView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    if request.method == 'POST':
        form = UploadEducationForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES['content']:
            form.save()
            return redirect('cadmineducation')
    else:
        form = UploadEducationForm(initial={'clinicid': clinicid})
    return render(request, "clinicadmin/uploadeducation.html", {'form': form})

@user_passes_test(usertype_check)
def UploadPromotionView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    if request.method == 'POST':
        form = UploadPromotionForm(request.POST)
        if form.is_valid():
            msg = form.save()
            subject = msg.title + " (" + clinic.name + ")"
            sendlist = list(Subscriber.objects.all())
            message = (subject, msg.content, settings.DEFAULT_FROM_EMAIL, sendlist)
            #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [cd['recipient']])
            send_mass_mail((message,), fail_silently=False)
            return redirect('cadminpromotion')
    else:
        form = UploadPromotionForm(initial={'clinicid': clinicid})
    return render(request, "clinicadmin/uploadpromotion.html", {'form': form})

@user_passes_test(usertype_check)
def ClinicCalenderView(request):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    context = {}
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, d.month, clinicid)
    html_cal = cal.formatmonth(withyear=True)
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)
    return render(request, "clinicadmin/cliniccalender.html", context)

@user_passes_test(usertype_check)
def EditDoctorPasswordView(request,id):
    doctor = get_object_or_404(Doctor, user_account_id=id)
    account = doctor.user_account
    fkey = doctor.clinicid.id
    clinic = get_object_or_404(Clinic, id=fkey)
    if request.method == 'POST':
        form = ChangeDoctorPasswordForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data['password']
            pass2 = form.cleaned_data['password1']
            if pass1 == pass2:
                account.set_password(pass1)
                account.save()
                return redirect('cadmindocaccounts')
            else:
                messages.error(request, 'Passwords do not match')
    else:
        form = ChangeDoctorPasswordForm()
    return render(request, "clinicadmin/editdoctorpassword.html", {'form': form , 'clinic': clinic, 'doctor': doctor})

@user_passes_test(usertype_check)
def DeleteDoctorView(request,id):
    doctor = get_object_or_404(Doctor, user_account_id=id)
    account = doctor.user_account
    account.delete()
    return redirect('cadmindocaccounts')

@user_passes_test(usertype_check)
def DeleteAppointmentView(request,id):
    appt = get_object_or_404(Appointment, id=id)
    appt.slot.occupied = False
    appt.delete()
    return redirect('cadminappointments')

@user_passes_test(usertype_check)
def DeleteEducationView(request,id):
    educationmat = get_object_or_404(EducationMaterial, id=id)
    educationmat.delete()
    return redirect('cadmineducation')

@user_passes_test(usertype_check)
def DoctorScheduleView(request,id):
    doc = get_object_or_404(Doctor, user_account_id=id)
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
    context['id'] = id
    return render(request, "clinicadmin/doctorschedule.html", context)

@user_passes_test(usertype_check)
def DoctorSetScheduleView(request,id):
    doctor = get_object_or_404(Doctor, user_account_id=id)
    account = doctor.user_account
    clinicid = doctor.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    default = {
      'doctorid': doctor.user_account.id,
      'weekdaystart': clinic.openinghours.weekdaystart,
      'weekdayend': clinic.openinghours.weekdayend,
      'satstart': clinic.openinghours.satstart,
      'satend': clinic.openinghours.satend,
      'sunstart': clinic.openinghours.sunstart,
      'sunend': clinic.openinghours.sunend,
      'phstart': clinic.openinghours.phstart,
      'phend': clinic.openinghours.phend
    }
    if request.method == 'POST':
        form = DocSetScheduleForm(request.POST)
        if form.is_valid():
          form.save();
          return redirect('cadmindocaccounts')
    else:
        form = DocSetScheduleForm(initial=default)
    return render(request, "clinicadmin/setschecule.html", {'form': form})

@user_passes_test(usertype_check)
def DoctorEditScheduleView(request,id):
    doctor = get_object_or_404(Doctor, user_account_id=id)
    docschedule = get_object_or_404(DoctorSchedule, doctorid=id)
    default = {
      'doctorid': doctor.user_account.id,
      'weekdaystart': docschedule.weekdaystart,
      'weekdayend': docschedule.weekdayend,
      'satstart': docschedule.satstart,
      'satend': docschedule.satend,
      'sunstart': docschedule.sunstart,
      'sunend': docschedule.sunend,
      'phstart': docschedule.phstart,
      'phend': docschedule.phend
    }
    if request.method == 'POST':
        form = DocSetScheduleForm(request.POST, instance=docschedule)
        if form.is_valid():
          form.save();
          return redirect('cadmindocaccounts')
    else:
        form = DocSetScheduleForm(initial=default)
    return render(request, "clinicadmin/editschecule.html", {'form': form})

@user_passes_test(usertype_check)
def LoadPublicHoildayView(request):
    year = datetime.now().year + 1
    for date, name in holidays.Singapore(years = year).items():
        ph, created = PublicHoliday.objects.get_or_create(name = name,date = date)
        if created:
            ph.save()
        else:
            messages.error(request, 'Duplicate Entry :'+ name)
    messages.info(request, "Public Holidays Loaded")
    return redirect('cadmincliniccalender')

@user_passes_test(usertype_check)
def CreateWorkingCalenderView(request):
    #todelete = Slot.objects.filter(datetimestart__month__gte=11)
    #todelete.delete()
    year = datetime.now().year
    sg_holidays = holidays.Singapore()
    now = date.today()
    #start_date = date(2021,11,1)
    #end_date = date(2021,11,30)
    #firstday = (now.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    #lastday = firstday.replace(day = calendar.monthrange(firstday.year, firstday.month)[1])
    start_date = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
    end_date = start_date.replace(day = calendar.monthrange(start_date.year, start_date.month)[1]) + timedelta(days=1)
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=request.user.id)
    clinicid = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=clinicid)
    slotcount = 0
    tz = timezone.get_current_timezone()
    if clinic.apptinterval != 0 and clinic.doctorinterval != 0:
      min = 60 / clinic.apptinterval
      for single_date in daterange(start_date, end_date):
        if single_date in sg_holidays:
          if clinic.openinghours.phstart is not None and clinic.openinghours.phend is not None:
            start = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.phstart), tz, True)
            end = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.phend), tz, True)
            while start<=end:
              for i in range(clinic.doctorinterval):
                slot = Slot.objects.create(clinicid=clinic,datetimestart=start,datetimeend=start+timedelta(minutes=min))
                slotcount += 1
              start += timedelta(minutes=min)
        elif single_date.isoweekday() >= 1 and single_date.isoweekday() <= 5:
          if clinic.openinghours.weekdaystart is not None and clinic.openinghours.weekdayend is not None:
            start = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.weekdaystart), tz, True)
            end = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.weekdayend), tz, True)
            while start<=end:
              for i in range(clinic.doctorinterval):
                slot = Slot.objects.create(clinicid=clinic,datetimestart=start,datetimeend=start+timedelta(minutes=min))
                slotcount += 1
              start += timedelta(minutes=min)
        elif single_date.isoweekday() == 6:
          if clinic.openinghours.satstart is not None and clinic.openinghours.satend is not None:
            start = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.satstart), tz, True)
            end = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.satend), tz, True)
            while start<=end:
              for i in range(clinic.doctorinterval):
                slot = Slot.objects.create(clinicid=clinic,datetimestart=start,datetimeend=start+timedelta(minutes=min))
                slotcount += 1
              start += timedelta(minutes=min)
        elif single_date.isoweekday() == 7:
          if clinic.openinghours.sunstart is not None and clinic.openinghours.sunend is not None:
            start = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.sunstart), tz, True)
            end = timezone.make_aware(datetime.combine(single_date, clinic.openinghours.sunend), tz, True)
            while start<=end:
              for i in range(clinic.doctorinterval):
                slot = Slot.objects.create(clinicid=clinic,datetimestart=start,datetimeend=start+timedelta(minutes=min))
                slotcount += 1
              start += timedelta(minutes=min)
    else:
      messages.error(request, 'Appointment Interval/Doctor Interval not set')
      return redirect('cadmincliniccalender')
    messages.info(request, "Working Calendar Created. Total Slots Created: " + str(slotcount))
    return redirect('cadmincliniccalender')

class DoctorCalendarView(generic.ListView):
    model = PublicHoliday
    template_name = 'clinicadmin/doctorschedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = DoctorCalendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['id'] = self.kwargs['id']
        return context

class ClinicCalendarView(generic.ListView):
    model = PublicHoliday
    template_name = 'clinicadmin/cliniccalender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

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

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)