from django.db import models
from django.contrib.auth.models import AbstractUser
from doctor.models import Specialty
from systemadmin.models import Clinic

# Create your models here.

class BaseUser(AbstractUser):
    pass
    # add additional fields in here
    name = models.CharField(max_length=255)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_clinicadmin = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_name(seld):
        return  self.name


class Patient(models.Model):
    phone = models.CharField(max_length=100)
    user_account = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user_account.name


class Doctor(models.Model):
    specialty = models.ManyToManyField(Specialty)
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    user_account = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user_account.name


class ClinicAdmin(models.Model):
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    user_account = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user_account.name
