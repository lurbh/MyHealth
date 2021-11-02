from django.shortcuts import render
from .forms import ClinicCreationForm, ClinicEditionForm, ChangePasswordForm
from .models import OpeningHours, Clinic, AdminRequest
from django.shortcuts import redirect, get_object_or_404
from users.forms import ClinicAdminForm, ClinicAdminChangeForm, ChangeClinicAdminPasswordForm
from users.models import ClinicAdmin, BaseUser
from django.db.models import Count
import sys
from django.contrib import messages

from django.contrib.auth.decorators import user_passes_test

def usertype_check(user):
    if user.is_authenticated:
        return user.is_superuser
    else:
        return False

# Create your views here.
@user_passes_test(usertype_check)
def OverviewView(request):
    clinics = Clinic.objects.all()
    count = ClinicAdmin.objects.values('clinicid').annotate(total=Count('clinicid')).order_by()
    clinicsadmin = {}
    for i in count:
        clinicname = get_object_or_404(Clinic, id=i['clinicid'])
        clinicsadmin[clinicname] = i['total']
        
    return render(request, "systemadmin/overview.html", {'clinics': clinics, 'clinicsadmin': clinicsadmin})

@user_passes_test(usertype_check)
def ClinicsView(request):
    clinics = Clinic.objects.all()
    return render(request, "systemadmin/clinics.html", {'clinics': clinics})

@user_passes_test(usertype_check)
def CreateClinicView(request):
    if request.method == 'POST':
        form = ClinicCreationForm(request.POST)
        if form.is_valid():
            openhrs = OpeningHours.objects.create()
            openhrs.save()
            clinic = Clinic.objects.create(openinghours = openhrs)
            clinic.name = form.cleaned_data['name']
            clinic.location = form.cleaned_data['location']
            clinic.type = form.cleaned_data['type']
            clinic.save()
            return redirect('sadminclinics')
    else:
        form = ClinicCreationForm()
    return render(request, "systemadmin/addclinic.html", {'form': form})

@user_passes_test(usertype_check)
def ClinicAdminsView(request):
    group = ClinicAdmin.objects.values('clinicid').annotate(total=Count('clinicid')).order_by()
    clinicsadmin = []
    for i in group:
        cid = i['clinicid']
        clinicname = get_object_or_404(Clinic, id=cid)
        count = i['total']
        cadmin = {
          "id": cid,
          "name": clinicname,
          "count": count
        }
        clinicsadmin.append(cadmin)
    return render(request, "systemadmin/clinicadmin.html" , {'clinicsadmin': clinicsadmin})

@user_passes_test(usertype_check)
def AddClinicAdminView(request):
    if request.method == 'POST':
        clinicform = ClinicAdminForm(request.POST)
        if clinicform.is_valid():
            clinicform.save()
            return redirect('sadmincadmins')
    else:
        clinicform = ClinicAdminForm()
    return render(request, "systemadmin/addclinicadmin.html", {'form': clinicform})

@user_passes_test(usertype_check)
def AddClinicAdminIDView(request,id):
    clinic = get_object_or_404(Clinic, id=id)
    if request.method == 'POST':
        clinicform = ClinicAdminForm(request.POST)
        if clinicform.is_valid():
            clinicform.save()
            return redirect('sadminclinic', id=id)
    else:
        clinicform = ClinicAdminForm(initial={'clinic': id })
    return render(request, "systemadmin/addclinicadmin.html", {'form': clinicform})

@user_passes_test(usertype_check)
def AdminRequestView(request):
    adminrequests = AdminRequest.objects.all()
    return render(request, "systemadmin/adminrequest.html" , {'adminrequests': adminrequests})

@user_passes_test(usertype_check)
def AddClinicAdminRequestView(request,id):
    adrequest = get_object_or_404(AdminRequest, id=id)
    messages.info(request, "Default Password: " + adrequest.password)
    if request.method == 'POST':
        clinicform = ClinicAdminForm(request.POST)
        if clinicform.is_valid():
            clinicform.save()
            adrequest.delete()
            return redirect('sadmincadminrequest')
    else:
        clinicform = ClinicAdminForm(initial={'clinic': adrequest.clinicid, 'username': adrequest.username, 'name': adrequest.name })
    return render(request, "systemadmin/addclinicadminreq.html", {'form': clinicform, 'adrequest': adrequest })

@user_passes_test(usertype_check)
def ClinicView(request,id):
    clinic = get_object_or_404(Clinic, id=id)
    clinicadmins = ClinicAdmin.objects.filter(clinicid=id)
    count = ClinicAdmin.objects.filter(clinicid=id).count()
    return render(request, "systemadmin/clinic.html", {'clinic': clinic , 'clinicadmins': clinicadmins, 'count': count })

@user_passes_test(usertype_check)
def EditClinicView(request,id):
    clinic = get_object_or_404(Clinic, id=id)
    if request.method == 'POST':
        form = ClinicEditionForm(request.POST)
        if form.is_valid():
            clinic.name = form.cleaned_data['name']
            clinic.location = form.cleaned_data['location']
            clinic.type = form.cleaned_data['type']
            clinic.save()
            return redirect('sadminclinics')
    else:
        cname = clinic.name
        ctype = clinic.type
        clocation = clinic.location
        form = ClinicEditionForm(initial={'name': cname, 'type': ctype, 'location': clocation })
    return render(request, "systemadmin/editclinic.html", {'clinic': clinic , 'form': form})

@user_passes_test(usertype_check)
def EditClinicAdminView(request,id):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=id)
    account = cadmin.user_account
    fkey = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=fkey)
    if request.method == 'POST':
        form = ClinicAdminChangeForm(request.POST, instance=account)
        if form.is_valid():
            #account.name = form.cleaned_data['name']
            #account.username = form.cleaned_data['username']
            form.save()
            return redirect('sadminclinic', id=fkey)
    else:
        caname = cadmin.user_account.name
        causername = cadmin.user_account.username
        form = ClinicAdminChangeForm(initial={'name': caname, 'username': causername })
    return render(request, "systemadmin/editclinicadmin.html", {'form': form , 'clinic': clinic})

@user_passes_test(usertype_check)
def DeleteClinicView(request,id):
    clinic = get_object_or_404(Clinic, id=id)
    clinicadmins = ClinicAdmin.objects.filter(clinicid=id)
    for ca in clinicadmins:
        ca.user_account.delete()
    clinic.openinghours.delete()
    clinic.delete()
    return redirect('sadminclinics')

@user_passes_test(usertype_check)
def DeleteClinicAdminView(request,id):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=id)
    account = cadmin.user_account
    fkey = cadmin.clinicid.id
    account.delete()
    return redirect('sadminclinic', id=fkey)
  
@user_passes_test(usertype_check)  
def DeleteClinicAdminRequestView(request,id):
    adminrequest = get_object_or_404(AdminRequest, id=id)
    adminrequest.delete()
    return redirect('sadmincadminrequest')
   
@user_passes_test(usertype_check)   
def EditClinicAdminPasswordView(request,id):
    cadmin = get_object_or_404(ClinicAdmin, user_account_id=id)
    account = cadmin.user_account
    fkey = cadmin.clinicid.id
    clinic = get_object_or_404(Clinic, id=fkey)
    if request.method == 'POST':
        form = ChangeClinicAdminPasswordForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data['password']
            pass2 = form.cleaned_data['password1']
            if pass1 == pass2:
                account.set_password(pass1)
                account.save()
                return redirect('sadminclinic', id=fkey)
            else:
                messages.error(request, 'Passwords do not match')
    else:
        form = ChangeClinicAdminPasswordForm()
    return render(request, "systemadmin/editclinicadminpassword.html", {'form': form , 'clinic': clinic, 'cadmin': cadmin})