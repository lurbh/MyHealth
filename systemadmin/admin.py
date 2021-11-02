from django.contrib import admin
from .models import OpeningHours, Clinic, AdminRequest

# Register your models here.
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(OpeningHours, OpeningHoursAdmin)

class ClinicAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'type']

admin.site.register(Clinic, ClinicAdmin)

class AdminRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'name', 'clinicid']

admin.site.register(AdminRequest, AdminRequestAdmin)
