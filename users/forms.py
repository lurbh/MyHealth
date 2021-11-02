# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Patient, BaseUser, Doctor, ClinicAdmin
from django.db import transaction
from systemadmin.models import Clinic
from django.forms import ModelForm
from doctor.models import Specialty
from django.shortcuts import get_object_or_404
from general.models import *

class PatientCreationForm(UserCreationForm):
    phone = forms.CharField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = BaseUser
        fields = ('username','name','email')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user_account=user)
        patient.phone = self.cleaned_data['phone']
        patient.save()
        sub = Subscriber.objects.get_or_create(email=user.email)
        sub.save()
        return user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = BaseUser
        fields = ('username','name','email')

class PatientChangeForm(ModelForm):
    phone = forms.CharField(required=True)
    
    class Meta():
        model = BaseUser
        fields = ('username','name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
        patient = get_object_or_404(Patient, user_account_id=user.id)
        patient.phone = self.cleaned_data['phone']
        patient.save()
        return user

class ClinicAdminForm(UserCreationForm):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    
    class Meta(UserCreationForm.Meta):
        model = BaseUser
        fields = ('username','name')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_clinicadmin = True
        user.save()
        clinicadmin = ClinicAdmin.objects.create(user_account=user,clinicid=self.cleaned_data['clinic'])
        clinicadmin.save()
        return user

class ClinicAdminChangeForm(ModelForm):
    
    class Meta():
        model = BaseUser
        fields = ('username','name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.username = self.cleaned_data['username']
        user.save()
        return user

class ChangeClinicAdminPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(),required=True)


class DoctorForm(UserCreationForm):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    specialty = forms.ModelMultipleChoiceField(queryset=Specialty.objects.all())
    
    class Meta(UserCreationForm.Meta):
        model = BaseUser
        fields = ('username','name')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user_account=user,clinicid=self.cleaned_data['clinic'])
        doctor.specialty.clear()
        doctor.specialty.add(*self.cleaned_data['specialty'])
        doctor.save()
        return user
        
class DoctorChangeForm(ModelForm):
    specialty = forms.ModelMultipleChoiceField(queryset=Specialty.objects.all())
    
    class Meta():
        model = BaseUser
        fields = ('username','name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.username = self.cleaned_data['username']
        user.save()
        doctor = get_object_or_404(Doctor, user_account_id=user.id)
        doctor.specialty.clear()
        doctor.specialty.add(*self.cleaned_data['specialty'])
        doctor.save()
        return user

class ChangeDoctorPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(),required=True)

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput(),required=True)
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(),required=True)