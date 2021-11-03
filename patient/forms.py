from django import forms
from django.forms import ModelForm
from .models import Appointment
from users.models import Doctor

class AppointmentAdminForm(ModelForm):
    
    class Meta():
        model = Appointment
        fields = ('patientid','clinicid','type','doctorid','room')
    
    def __init__(self, *args, **kwargs):
        super(AppointmentAdminForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'inputappointment'
        self.fields['doctorid'].required = False

class AppointmentForm(ModelForm):
    
    class Meta():
        model = Appointment
        fields = ('patientid','clinicid','type','doctorid')
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'inputbooking'
        self.fields['doctorid'].required = False
        self.fields['doctorid'].queryset = Doctor.objects.none()
 
class AppointmentRateForm(ModelForm):
    
    class Meta():
        model = Appointment
        fields = ('rating',)
    
    def __init__(self, *args, **kwargs):
        super(AppointmentRateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'inputrating'
