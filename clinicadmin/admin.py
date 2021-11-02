from django.contrib import admin
from .models import *

# Register your models here.
class EducationMaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'uploaddate']

admin.site.register(EducationMaterial, EducationMaterialAdmin)

class PromotionalMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'senddate']

admin.site.register(PromotionalMessage, PromotionalMessageAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor', 'location']

admin.site.register(Room, RoomAdmin)

class PublicHolidayAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date']

admin.site.register(PublicHoliday, PublicHolidayAdmin)

class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctorid']

admin.site.register(DoctorSchedule, DoctorScheduleAdmin)

class SlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'clinicid', 'datetimestart', 'datetimeend']

admin.site.register(Slot, SlotAdmin)

class AppointmentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']

admin.site.register(AppointmentType, AppointmentTypeAdmin)