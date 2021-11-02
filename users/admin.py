from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .forms import PatientCreationForm, CustomUserChangeForm
from .models import BaseUser, Patient, Doctor, ClinicAdmin

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(BaseUser, CustomUserAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Patient, PatientAdmin)

class DoctorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Doctor,DoctorAdmin)

class ClinicAdminAdmin(admin.ModelAdmin):
    pass

admin.site.register(ClinicAdmin, ClinicAdminAdmin)