from django.contrib import admin
from .models import Specialty

# Register your models here.
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['id', 'specialty']

admin.site.register(Specialty, SpecialtyAdmin)