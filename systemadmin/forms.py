from django import forms
from .models import Clinic, OpeningHours
from django.db import transaction
from django.forms import ModelForm
from users.models import ClinicAdmin, BaseUser

class ClinicCreationForm(ModelForm):
    
    class Meta:
        model = Clinic
        fields = ('name','location','type')
        

class ClinicEditionForm(ModelForm):
    
    class Meta:
        model = Clinic
        fields = ('name','location','type')
        

class ChangePasswordForm(ModelForm):
    
    class Meta:
        model = BaseUser
        fields = ('username','name')
        