from django.db import models
from users.models import Patient, Doctor
from systemadmin.models import Clinic
from clinicadmin.models import AppointmentType, Slot, Room
from datetime import date, datetime, timedelta
from smart_selects.db_fields import ChainedForeignKey 
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Appointment(models.Model):
    patientid = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    type = models.ForeignKey(AppointmentType, on_delete=models.CASCADE)
    doctorid = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField (default=0,validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    confirm = models.BooleanField(default=False)
    canconfirm = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.patientid) + str(self.clinicid) + str(self.slot)

