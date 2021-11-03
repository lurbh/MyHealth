from django import forms
from django.forms import ModelForm
from systemadmin.models import Clinic, OpeningHours, AdminRequest
from .models import *

class ClinicOverviewForm(ModelForm):
    
    class Meta:
        model = Clinic
        fields = ('name','address','phone','email','apptinterval','doctorinterval','image')
    
    def __init__(self, *args, **kwargs):
        super(ClinicOverviewForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class OpeningHoursForm(ModelForm):
    
    class Meta:
        model = OpeningHours
        fields = ('weekdaystart','weekdayend','satstart','satend','sunstart','sunend','phstart','phend')
    
    def __init__(self, *args, **kwargs):
        super(OpeningHoursForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget = forms.TimeInput(format='%H:%M')
            visible.field.widget.attrs['class'] = 'timepicker'
        self.fields['satstart'].required = False
        self.fields['satend'].required = False
        self.fields['sunstart'].required = False
        self.fields['sunend'].required = False
        self.fields['phstart'].required = False
        self.fields['phend'].required = False


class AdminRequestForm(ModelForm):
    
    class Meta:
        model = AdminRequest
        fields = ('clinicid','username','name','password')


class UploadEducationForm(ModelForm):
    
    class Meta:
        model = EducationMaterial
        fields = ('title','clinicid','content')

class UploadPromotionForm(ModelForm):
    
    class Meta:
        model = PromotionalMessage
        fields = ('title','clinicid','content')

class DocSetScheduleForm(ModelForm):
    
    class Meta:
        model = DoctorSchedule
        fields = ('doctorid','weekdaystart','weekdayend','satstart','satend','sunstart','sunend','phstart','phend')
    
    def __init__(self, *args, **kwargs):
        super(DocSetScheduleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget = forms.TimeInput(format='%H:%M')
            visible.field.widget.attrs['class'] = 'timepicker scheduleinput'
        self.fields['satstart'].required = False
        self.fields['satend'].required = False
        self.fields['sunstart'].required = False
        self.fields['sunend'].required = False
        self.fields['phstart'].required = False
        self.fields['phend'].required = False