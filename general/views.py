from django.shortcuts import render
from systemadmin.models import Clinic
from patient.models import Appointment
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from clinicadmin.models import EducationMaterial
from doctor.models import Specialty
from users.models import Doctor
from .forms import SubscribeForm, ContactForm
from .models import *
from django.core.mail import send_mail

from django.conf import settings
# Create your views here.

def HomeView(request):
    if request.method == 'POST':
      subform = SubscribeForm(request.POST)
      if subform.is_valid():
        email = subform.cleaned_data['email']
        sub = Subscriber.objects.create(email=email)
        sub.save()
        subform = SubscribeForm()
    else:
        subform = SubscribeForm()
    return render(request, "general/home.html", {'subform': subform})

def AboutusView(request):
    if request.method == 'POST':
      subform = SubscribeForm(request.POST)
      if subform.is_valid():
        email = subform.cleaned_data['email']
        sub = Subscriber.objects.create(email=email)
        sub.save()
        subform = SubscribeForm()
    else:
        subform = SubscribeForm()
    return render(request, "general/aboutus.html", {'subform': subform})
    
def ContactusView(request):
    if request.method == 'POST':
      subform = SubscribeForm(request.POST)
      form = ContactForm(request.POST)
      if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data['message']
        subject = "Contact From " + name + " Email: " + email + " Phone: " + phone
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
        form = ContactForm()
      if subform.is_valid():
        email = subform.cleaned_data['email']
        sub = Subscriber.objects.create(email=email)
        sub.save()
        subform = SubscribeForm()
    else:
        subform = SubscribeForm()
        form = ContactForm()
    return render(request, "general/contactus.html", {'form': form, 'subform': subform})
    
def ClinicsView(request):
    clinics = Clinic.objects.all()
    educationlist = {}
    specialties = Specialty.objects.all()
    for clinic in clinics:
      appointments = Appointment.objects.filter(clinicid=clinic.id,rating__gt=0)
      avrrating = appointments.aggregate(Avg('rating'))
      rating = avrrating['rating__avg']
      if rating is not None:
        clinic.rating = round(rating,2)
      else:
        clinic.rating = rating
      cliniceducation = EducationMaterial.objects.filter(clinicid=clinic.id)
      educationlist[clinic.id] = cliniceducation
    location = request.GET.get('location', False)
    if location == 'all':
      location = False
    if location != False:
      clinics = clinics.filter(location=location)
    specialist = request.GET.get('inputspecialist', False)
    if specialist != False:
      doctors = Doctor.objects.filter(specialty__in=specialist)
      c = []
      for doc in doctors:
        if doc.clinicid.id not in c:
          c.append(doc.clinicid.id)
      clinics = clinics.filter(id__in=c)
    if request.method == 'POST':
      subform = SubscribeForm(request.POST)
      if subform.is_valid():
        email = subform.cleaned_data['email']
        sub = Subscriber.objects.create(email=email)
        sub.save()
        subform = SubscribeForm()
    else:
        subform = SubscribeForm()
    return render(request, "general/clinics.html", {'clinics': clinics, 'educationlist': educationlist, 'specialties': specialties, 'subform': subform})

def SubscribeView(request):
    return redirect('/path/to/current/page/')