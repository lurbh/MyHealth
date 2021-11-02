from django.db import models
from systemadmin.models import Clinic
from users.models import Doctor
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

# Create your models here.
class EducationMaterial(models.Model):
    title = models.CharField(max_length=100)
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    content = models.FileField(upload_to="files/educationmaterials")
    uploaddate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class PromotionalMessage(models.Model):
    title = models.CharField(max_length=100)
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    content = models.TextField()
    senddate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Room(models.Model):
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    floor = models.IntegerField()
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return "Floor: " + str(self.floor) + " Room: " + self.location

class PublicHoliday(models.Model):
    name = models.CharField(max_length=100,)
    date = models.DateField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'date'], name='Public Holiday')
        ]
    
    def __str__(self):
        return self.name + self.date

class DoctorSchedule(models.Model):
    doctorid = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    weekdaystart = models.TimeField(null=True)
    weekdayend = models.TimeField(null=True)
    satstart = models.TimeField(null=True)
    satend = models.TimeField(null=True)
    sunstart = models.TimeField(null=True)
    sunend = models.TimeField(null=True)
    phstart = models.TimeField(null=True)
    phend = models.TimeField(null=True)
    
    def __str__(self):
        return self.doctorid.user_account.username

class Slot(models.Model):
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    datetimestart = models.DateTimeField()
    datetimeend = models.DateTimeField(default=datetime.now())
    occupied = models.BooleanField(default=False)
     
    def __str__(self):
        return self.clinicid.name + " " + ((self.datetimestart)+ timedelta(hours=8)).strftime('%d/%m/%Y %H:%M')

class AppointmentType(models.Model):
    type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.type