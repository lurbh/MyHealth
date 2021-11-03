from django.contrib import admin
from .models import *

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id','patientid', 'clinicid', 'slot']

admin.site.register(Appointment, AppointmentAdmin)