from django.db import models

# Create your models here.

class Specialty(models.Model):
    specialty = models.CharField(max_length=100)
    
    def __str__(self):
        return self.specialty