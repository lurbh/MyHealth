from django.db import models
import datetime
import holidays

d = datetime.time(00, 00, 00)

# Create your models here.
class OpeningHours(models.Model):
    weekdaystart = models.TimeField(null=True)
    weekdayend = models.TimeField(null=True)
    satstart = models.TimeField(null=True)
    satend = models.TimeField(null=True)
    sunstart = models.TimeField(null=True)
    sunend = models.TimeField(null=True)
    phstart = models.TimeField(null=True)
    phend = models.TimeField(null=True)
    
    def __str__(self):
        return str(self.id)


class Clinic(models.Model):
    LOCATION_CHOICES = (
        ('North','North'),
        ('South', 'South'),
        ('Central','Central'),
        ('East','East'),
        ('West','West'),
    )
    TYPE_CHOICES = (
        ('Normal','Normal'),
        ('Specialist', 'Specialist'),
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    apptinterval = models.IntegerField(default=0)
    doctorinterval = models.IntegerField(default=0)
    openinghours = models.OneToOneField(OpeningHours, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/clinics",blank=True)
    location = models.CharField(max_length=100, choices= LOCATION_CHOICES, default='central')
    type = models.CharField(max_length=100, choices= TYPE_CHOICES, default='normal')
    
    def __str__(self):
        return self.name

class AdminRequest(models.Model):
    clinicid = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username + self.clinicid.name
